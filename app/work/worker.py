import threading
import queue

from app.algorithms import ASR, AsrResult, extract_audio_from_video


class Worker:
    def __init__(self) -> None:
        self.asr = ASR()

        self.worker_thread = None
        self.is_running = False
        self.task_queue = queue.Queue()
        self.lock = threading.Lock()
        self.result_dict = {}

    def join(self) -> None:
        self.task_queue.join()
        self.task_queue.put(None)
        if self.worker_thread:
            self.worker_thread.join()

    def add_task(self, session_id: str, file_path: str, file_type: str) -> None:
        with self.lock:
            self.task_queue.put((session_id, file_path, file_type))
            if not self.is_running:
                self.is_running = True
                self.worker_thread = threading.Thread(target=self._process_tasks)
                self.worker_thread.start()

    def _process_tasks(self) -> None:
        while True:
            session_id, file_path, file_type = self.task_queue.get()
            if session_id is None:
                break
            self._asr_task(session_id, file_path, file_type)
            self.task_queue.task_done()
        self.is_running = False

    def _asr_task(self, session_id: str, file_path: str, file_type: str) -> None:
        if file_type == "video":
            file_path = extract_audio_from_video(file_path)

        detail = self.asr(file_path)
        with self.lock:
            self.result_dict[session_id] = detail

    def get_result(self, session_id: str) -> AsrResult:
        with self.lock:
            result = self.result_dict.get(session_id)
            del self.result_dict[session_id]
        return result
