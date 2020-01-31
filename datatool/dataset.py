# region PublicActivityRoutines
    def get_activities_by_indices(self, activity_ids):
        """Get a group of activities by their corresponding indices

        Args:
            activity_ids (:obj:`list` of :obj:`int`): A list of activity indices

        Returns:
            :obj:`list` of :obj:`str`: A list of activity labels in the same order
        """
        return [self.get_activity_by_index(cur_id) for cur_id in activity_ids]

    def get_activity_by_index(self, activity_id):
        """Get Activity name by their index

        Args:
            activity_id (:obj:`int`): Activity index

        Returns:
            :obj:`str`: Activity label
        """
        for activity_label in self.activity_list.keys():
            if activity_id == self.activity_list[activity_label]['index']:
                return activity_label
        logger.error('Failed to find activity with index %d' % activity_id)
        return ""

    def get_activity_index(self, activity_label):
        """Get Index of an activity

        Args:
            activity_label (:obj:`str`): Activity label

        Returns:
            :obj:`int`: Activity index (-1 if not found or not enabled)
        """
        if activity_label in self.activity_list:
            return self.activity_list[activity_label]['index']
        else:
            return -1

    def get_enabled_activities(self):
        """Get label list of all enabled activities

        Returns:
            :obj:`list` of :obj:`str`: list of activity labels
        """
        enabled_activities_list = []
        for activity_label in self.activity_list.keys():
            if self.activity_list[activity_label]['enable']:
                enabled_activities_list.append(activity_label)
        return enabled_activities_list

    def get_activity_color(self, activity_label):
        """Find the color string for the activity.

        Args:
            activity_label (:obj:`str`): activity label

        Returns:
            :obj:`str`: RGB color string
        """
        if self.is_legacy:
            # Pick the color from color list based on the activity index
            activity_index = self.get_activity_index(activity_label)
            if activity_index >= 0:
                return self._COLORS[activity_index % len(self._COLORS)]
            else:
                return '#C8C8C8'   # returns grey
        else:
            return self.home.get_activity_color(activity_label)

    def enable_activity(self, activity_label):
        """Enable an activity

        Args:
            activity_label (:obj:`str`): Activity label

        Returns:
            :obj:`int`: The index of the enabled activity
        """
        if activity_label in self.activity_list:
            logger.debug('Enable Activity %s' % activity_label)
            self.activity_list[activity_label]['enable'] = True
            self._assign_activity_indices()
            return self.activity_list[activity_label]['index']
        else:
            logger.error('Activity %s not found' % activity_label)
            return -1

    def disable_activity(self, activity_label):
        """Disable an activity

        Args:
            activity_label (:obj:`str`): Activity label
        """
        if activity_label in self.activity_list:
            logger.debug('Disable Activity %s' % activity_label)
            self.activity_list[activity_label]['enable'] = False
            self.activity_list[activity_label]['index'] = -1
            self._assign_activity_indices()
        else:
            logger.error('Activity %s not found' % activity_label)
    # endregion

    # region PublicSensorRoutines
    def enable_sensor(self, sensor_name):
        """Enable a sensor

        Args:
            sensor_name (:obj:`str`): Sensor Name

        Returns
            :obj:`int`: The index of the enabled sensor
        """
        if sensor_name in self.sensor_list:
            logger.debug('Enable Sensor %s' % sensor_name)
            self.sensor_list[sensor_name]['enable'] = True
            self._assign_sensor_indices()
            return self.sensor_list[sensor_name]['index']
        else:
            logger.error('Failed to find sensor %s' % sensor_name)
            return -1

    def disable_sensor(self, sensor_name):
        """Disable a sensor

        Args:
            sensor_name (:obj:`str`): Sensor Name
        """
        if sensor_name in self.sensor_list:
            logger.debug('Disable Sensor %s' % sensor_name)
            self.sensor_list[sensor_name]['enable'] = False
            self.sensor_list[sensor_name]['index'] = -1
            self._assign_sensor_indices()
        else:
            logger.error('Failed to find sensor %s' % sensor_name)

    def get_sensor_by_index(self, sensor_id):
        """Get the name of sensor by index

        Args:
            sensor_id (:obj:`int`): Sensor index

        Returns:
            :obj:`str`: Sensor name
        """
        for sensor_name in self.sensor_list.keys():
            if self.sensor_list[sensor_name]['index'] == sensor_id:
                return sensor_name
        logger.error('Failed to find sensor with index %d' % sensor_id)
        return ''

    def get_sensor_index(self, sensor_name):
        """Get Sensor Index

        Args:
            sensor_name (:obj:`str`): Sensor Name

        Returns:
            :obj:`int`: Sensor index (-1 if not found or not enabled)
        """
        if sensor_name in self.sensor_list:
            return self.sensor_list[sensor_name]['index']
        else:
            return -1

    def get_enabled_sensors(self):
        """Get the names of all enabled sensors

        Returns:
            :obj:`list` of :obj:`str`: List of sensor names
        """
        enabled_sensor_array = []
        for sensor_label in self.sensor_list.keys():
            if self.sensor_list[sensor_label]['enable']:
                enabled_sensor_array.append(sensor_label)
        return enabled_sensor_array
    # endregion


    # region PickleState
    def __getstate__(self):
        """Save x as sparse matrix if the density of x is smaller than 0.5
        """
        state = self.__dict__.copy()
        if self.x is not None:
            density_count = np.count_nonzero(self.x)
            density = float(density_count) / self.x.size
            if density < 0.5:
                state['x'] = sp.csr_matrix(state['x'])
        return self.__dict__

    def __setstate__(self, state):
        """Set state from pickled file
        """
        if sp.issparse(state['x']):
            state['x'] = state['x'].todense()
        self.__dict__.update(state)
    # endregion

# region Summary
    def summary(self):
        """Print summary of loaded datasets
        """
        print('Dataset Path: %s' % self.data_path)
        print('Sensors: %d' % len(self.sensor_list))
        print('Sensors enabled: %d' % len(self.get_enabled_sensors()))
        print('Activities: %d' % len(self.activity_list))
        print('Activities enabled: %d' % len(self.get_enabled_activities()))
        print('loaded events: %d' % len(self.event_list))
    # endregion

    _COLORS = ('#b20000, #56592d, #acdae6, #cc00be, #591616, #d5d9a3, '
               '#007ae6, #4d0047, #a67c7c, #2f3326, #00294d, #b35995, '
               '#ff9180, #1c330d, #73b0e6, #f2b6de, #592400, #6b994d, '
               '#1d2873, #ff0088, #cc7033, #50e639, #0000ff, #7f0033, '
               '#e6c3ac, #00d991, #c8bfff, #592d3e, #8c5e00, #80ffe5, '
               '#646080, #d9003a, #332200, #397367, #6930bf, #33000e, '
               '#ffbf40, #3dcef2, #1c0d33, #8c8300, #23778c, #ba79f2, '
               '#e6f23d, #203940, #302633').split(',')

    # region InternalActivityListManagement
    def _add_activity(self, label):
        """Add activity to :attr:`activity_list`

        Args:
            label (:obj:`str`): activity label

        Returns:
            :obj:`int`: activity index
        """
        if label not in self.activity_list:
            logger.debug('add activity class %s' % label)
            if self.is_legacy:
                self.activity_list[label] = {'name': label}
            else:
                self.activity_list[label] = self.home.get_activity(label)
                if self.activity_list[label] is None:
                    logger.warning('Failed to find information about activity %s' % label)
                    self.activity_list[label] = {'name': label}
            self.activity_list[label]['index'] = -1
            self.activity_list[label]['enable'] = True
            self.activity_list[label]['window_size'] = 30
            self._assign_activity_indices()
        return self.activity_list[label]['index']

    def _assign_activity_indices(self):
        """Assign index number to each activity enabled

        Returns:
            :obj:`int`: Number of enabled activities
        """
        _enabled_activities_list = []
        for label in self.activity_list.keys():
            activity = self.activity_list[label]
            if activity['enable']:
                _enabled_activities_list.append(label)
            else:
                activity['index'] = -1
        _enabled_activities_list.sort()
        i = 0
        for label in _enabled_activities_list:
            self.activity_list[label]['index'] = i
            i += 1
        num_enabled_activities = len(_enabled_activities_list)
        logger.debug('Finished assigning index to activities. %d Activities enabled' % num_enabled_activities)
        return num_enabled_activities
    # endregion

    # region InternalSensorListManagement
    def _add_sensor(self, name):
        """Add Sensor to :attr:`sensor_list`

        Args:
            name (:obj:`str`): sensor name

        Returns:
            (:obj:`int`): sensor index
        """
        if name not in self.sensor_list:
            logger.debug('Add sensor %s to sensor list' % name)
            if self.is_legacy:
                self.sensor_list[name] = {'name': name}
            else:
                self.sensor_list[name] = self.home.get_sensor(name)
                if self.sensor_list[name] is None:
                    logger.error('Failed to find information about sensor %s' % name)
                    self.sensor_list[name] = {'name': name}
            self.sensor_list[name]['index'] = -1
            self.sensor_list[name]['enable'] = True
            self.sensor_list[name]['lastFireTime'] = None
            self._assign_sensor_indices()
        return self.sensor_list[name]['index']

    def _assign_sensor_indices(self):
        """Assign index to each enabled sensor

        Returns
            :obj:`int`: The number of enabled sensor
        """
        sensor_id = 0
        _enabled_sensor_list = []
        for sensor_label in self.sensor_list.keys():
            if self.sensor_list[sensor_label]['enable']:
                _enabled_sensor_list.append(sensor_label)
            else:
                self.sensor_list[sensor_label]['index'] = -1
        _enabled_sensor_list.sort()
        for sensor_label in _enabled_sensor_list:
            self.sensor_list[sensor_label]['index'] = sensor_id
            sensor_id += 1
        return sensor_id
    # endregion