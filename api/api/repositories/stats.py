from ..models.stat import Stat

class Stats():

    @staticmethod
    def get_or_create(year, month, day, period, handle):
        id = str(year) + str(month) + str(day) + '-' + handle

        stat = Stat.objects(id=id).first()

        if stat == None:
            stat = Stat(id=id)
            stat.year = year
            stat.month = month
            stat.day = day
            stat.period = period
            stat.handle = handle

        return stat
