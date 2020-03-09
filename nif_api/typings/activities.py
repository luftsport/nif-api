from .helpers import unpack
from .activity import Activity


class Activities:
    def __init__(self, activities):

        if isinstance(activities, dict) is not True and 'Activities' in activities:
            self.status, value = unpack(activities, 'Activities')
            if self.status is True:
                self.value = value.get('Activities', {}).get('Activity', [])
        elif isinstance(activities, dict) is not True and 'Activity' in activities:
            self.status, value = unpack(activities, 'Activity')
            if self.status is True:
                self.value = value.get('Activity', [])
        elif isinstance(activities, dict) is True and 'activity' in activities:
            self.value = activities.get('activity', [])
        else:
            self.value = []

        self._map()


    def _map(self):

        new_value = []
        for v in self.value:
            new_value.append(Activity(v).value)

        self.value = new_value
