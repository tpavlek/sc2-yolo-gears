import sc2reader, os, sys
from sc2reader.plugins.replay import APMTracker, SelectionTracker

sc2reader.register_plugin('Replay', APMTracker())

class ProcessedReplays:

        def __init__(self, username, path):
            """
            The processed replays object represents the collection of replays loaded by
            the user, and the processed data associated with it.

            self.apm is a dictionary keyed by date (yyyy-mm-dd hh:mm:ss) containing the 
            average APM on that datetime

            Self.wr is a dictionary ordered by the race played by the active player,
            then subdictionaries of the race played by the opponent, which each have
            a two-item list: wins and total games. (This is not a tuple because tuples are immutable) 
            
            >>> p = ProcessedReplays('bonywonix', 'replays/')
            >>> p.me
            'bonywonix'
            >>> type(p.replays) is list
            True
            >>> type(p.wr) is dict
            True
            >>> p.replays[0].real_type != '1v1'
            False
            """
            self.me = username 
            self.apm = {}
            self.wr = {'Zerg': {'Zerg': [0,0], 'Protoss': [0,0], 'Terran': [0,0]}, 
                    'Protoss': {'Zerg': [0, 0], 'Protoss': [0, 0], 'Terran': [0, 0]},
                    'Terran': {'Zerg': [0,0], 'Protoss': [0,0], 'Terran': [0,0]} } 
            self.processedWR = False
            self.replays = list()
            for replay in sc2reader.load_replays(path):
                if replay.real_type == '1v1':
                    self.replays.append(replay)
        
        def getAPM(self):
            """
            Takes the internal object state and returns a dictionary, with key datetime
            and value avg APM in the game at that datetime.
            
            NOTE: If two games are played at identical datetimes, the latter one will overwrite the first.
            As games are typically up to 30 min long and datetime is precise to the second, this
            will rarely occur, but it is possible. This prevents the same replay from being in the folder
            several times and skewing the data.
            """

            #we may in some cases call APM after the dict is already populated. 
            if self.apm != {}:
                return self.apm
            
            for replay in self.replays:
                for team in replay.teams:
                    for player in team:
                        if player.name == self.me:
                            avg_apm = list()
                            for minute in player.apm:
                                avg_apm.append(player.apm[minute])
                            self.apm[str(replay.date)] = sum(avg_apm)//len(avg_apm)

            return self.apm

        def getWinrates(self):

            if self.processedWR:
                return self.wr

            for replay in self.replays:
                for team in replay.teams:
                    for player in team:
                        print(player.result)
                        if player.result == 'Win':
                            winner = player
                        else:
                            loser = player

                if winner.name == self.me:
                    self.wr[winner.play_race][loser.play_race][0] += 1 
                    self.wr[winner.play_race][loser.play_race][1] += 1
                elif loser.name == self.me:
                    self.wr[loser.play_race][winner.play_race][1] += 1

            self.processedWR = True
            return self.getWinrates()

if __name__ == "__main__":
    import doctest
    doctest.testmod()
