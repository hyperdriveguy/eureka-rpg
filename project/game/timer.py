"""Keeps track of time between actions.
"""

class Timer:
    """Keep track of time in seconds.

    Stereotype: Information Holder

    Attributes:
        self._full (int): maximum time for the timer.
        self._countdown (int): current time remaining until done.
        self._paused (bool): whether to stop the countdown.
    """

    def __init__(self, secs=3):
        """Class constructor

        Args:
            secs (int, optional): number of seconds the timer should last. Defaults to 3.
        """
        self._full = secs
        self._countdown = secs
        self._paused = True

    def pause(self):
        """Stop the countdown.
        """
        self._paused = True

    def run(self):
        """Restart the countdown.
        """
        self._paused = False

    def update(self, delta_time):
        """Update the countdown.

        Args:
            delta_time (float): time to subtract from countdown in seconds.
        """
        if self.active:
            self._countdown -= delta_time

    def restart(self):
        """Restart the timer.
        """
        self._countdown = self._full
        self._paused = False

    @property
    def done(self):
        """Whether the timer has completed.

        Returns:
            bool: countdown has completed
        """
        return self._countdown <= 0 and not self._paused

    @property
    def stopped(self):
        """Whether the timer has fully stopped (completed and paused).

        Returns:
            bool: timer stopped
        """
        return self._countdown <= 0 and self._paused

    @property
    def active(self):
        """Whether timer is active (incomplete and not paused).

        Returns:
            bool: timer active
        """
        return self._countdown > 0 and not self._paused

    @property
    def is_paused(self):
        """Whether timer has paused the countdown.

        Returns:
            bool: paused
        """
        return self._paused
