import threading
import time

from photosorter.application.cancellation_token import CancellationToken


def test_not_cancelled_and_not_paused_by_default() -> None:
    token = CancellationToken()

    assert token.is_cancelled is False
    assert token.is_paused is False


def test_cancel_sets_is_cancelled() -> None:
    token = CancellationToken()

    token.cancel()

    assert token.is_cancelled is True


def test_wait_if_paused_blocks_until_resume() -> None:
    token = CancellationToken()
    token.pause()
    reached = threading.Event()

    def _wait() -> None:
        token.wait_if_paused()
        reached.set()

    thread = threading.Thread(target=_wait)
    thread.start()
    try:
        assert not reached.wait(timeout=0.2)  # sigue bloqueado mientras esta pausado

        token.resume()

        assert reached.wait(timeout=1.0)
        assert token.is_paused is False
    finally:
        thread.join(timeout=1.0)


def test_cancel_unblocks_a_paused_wait() -> None:
    token = CancellationToken()
    token.pause()
    reached = threading.Event()

    def _wait() -> None:
        token.wait_if_paused()
        reached.set()

    thread = threading.Thread(target=_wait)
    thread.start()
    try:
        assert not reached.wait(timeout=0.2)

        token.cancel()

        assert reached.wait(timeout=1.0)
        assert token.is_cancelled is True
    finally:
        thread.join(timeout=1.0)


def test_resume_without_pause_is_a_noop() -> None:
    token = CancellationToken()

    token.resume()

    assert token.is_paused is False
    start = time.monotonic()
    token.wait_if_paused()
    assert time.monotonic() - start < 0.2
