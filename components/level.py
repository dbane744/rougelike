class Level:
    def __init__(self, current_level=1, current_xp=0, level_up_base=200, level_up_factor=150):
        #TODO place xp numbers in constants dictionary.
        """
        Tracks the current xp and the xp required to level up for the player.
        :param current_level:
        :param current_xp:
        :param level_up_base:
        :param level_up_factor:
        """
        self.current_level = current_level
        self.current_xp = current_xp
        self.level_up_base = level_up_base
        self.level_up_factor = level_up_factor

    @property
    def experience_to_next_level(self):
        """
        Returns the number of exp points the player needs to level up.
        :param self:
        :return:
        """
        return self.level_up_base + self.current_level * self.level_up_factor

    def add_xp(self, xp):
        """
        Adds xp to the player's current xp.
        If the xp exceeds the xp needed to level up the character will level up and retain any excess xp.
        :param self:
        :param xp:
        :return: Returns True if the player levels up.
        """

        self.current_xp +=  xp

        if self.current_xp > self.experience_to_next_level:
            self.current_xp -= self.experience_to_next_level
            self.current_level += 1

            return True
        else:
            return False
