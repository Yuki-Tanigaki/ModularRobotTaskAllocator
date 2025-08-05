from typing import Type, Any

def find_subclasses_by_name(base_class: Type[Any]) -> dict[str, Type[Any]]:
    """
    指定された基底クラスのすべてのサブクラスを探索し、クラス名をキーとする辞書を返す

    :param base_class: 基底クラス
    :return: クラス名をキー、クラスオブジェクトを値とする辞書
    """
    subclasses: dict[str, Type[Any]] = {}
    for cls in base_class.__subclasses__():
        subclasses[cls.__name__] = cls  # クラス名 (__name__) をキーとして登録
    return subclasses

def get_class_init_args(cls: Type[Any], input_data: dict[str, Any], name: str) -> dict[str, Any]:
    """ clsの __init__ 引数にinput_dataを成形 """
    signature = inspect.signature(cls.__init__)
    init_args = [param for param in signature.parameters]
    # 渡すべき引数をフィルタリング
    filtered_args = {
        k: v for k, v in input_data.items() if k in init_args
    }
    filtered_args.update({NAME: name})

    return filtered_args

def enum_constructor(loader: Any, tag_suffix: str, node: yaml.Node) -> Any:
    """ Enum辞書の読み込みハンドラ """
    tag_name = tag_suffix.lstrip('!')
    enum_class = enum_classes.get(tag_name)
    if not isinstance(enum_class, type) or not issubclass(enum_class, Enum):
        raise_with_log(ValueError, f"!{tag_name} is not a valid Enum type")
    
    if isinstance(node, yaml.ScalarNode):
        key = loader.construct_scalar(node)
        return enum_class[key]

    elif isinstance(node, yaml.MappingNode):
        raw_mapping = loader.construct_mapping(node)
        return {
            enum_class[key]: raw_mapping.get(key, 0.0) for key in enum_class.__members__
        }

    else:
        raise raise_with_log(TypeError, f"Unsupported YAML node type for tag '!{tag_name}': {type(node)}")