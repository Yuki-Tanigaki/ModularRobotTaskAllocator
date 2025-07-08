import inspect
from typing import NoReturn
import logging

def setup_logger(logfile: str):
    formatter = logging.Formatter(
        '%(asctime)s [%(levelname)s] %(name)s.%(funcName)s(): %(message)s'
    )

    # ルートロガーの設定
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    # コンソール出力
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # ファイル出力
    file_handler = logging.FileHandler(logfile)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # 重複登録を避けるために既存のハンドラーをクリア
    if root_logger.hasHandlers():
        root_logger.handlers.clear()

    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)

def raise_with_log(exc_type: type[Exception], message: str) -> NoReturn:
    # 呼び出し元のスタックフレームを取得（1つ上のフレーム）
    frame = inspect.currentframe()
    caller_frame = frame.f_back if frame else None

    # デフォルト値（取得失敗時）
    classname = "UnknownClass"
    funcname = "UnknownFunction"

    if caller_frame:
        funcname = caller_frame.f_code.co_name
        # self があるならクラス名を取得（メソッド内から呼ばれている場合）
        self_obj = caller_frame.f_locals.get('self', None)
        if self_obj:
            classname = type(self_obj).__name__
        else:
            classname = caller_frame.f_globals.get('__name__', "UnknownModule")


    logger = logging.getLogger(__name__)
    logger.error(f"[{exc_type.__name__}] {classname}.{funcname}(): {message}")
    raise exc_type(message)
