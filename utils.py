from collections import defaultdict

from shapely import distance as shp_distance

#


def group_by_distance(geom_list, dist_factor):

    groups = Groups(geom_list, dist_factor)

    return groups.export_geoms()


class Groups:
    #
    def __init__(self, geom_list, dist_factor):

        self.geom_list = geom_list
        self.dist_factor = dist_factor

        self.geom_index = dict(enumerate(geom_list))
        self.groups = defaultdict(set)

        for index in self.geom_index.keys():
            self._tick(index)

        self._merge()

    #
    def _tick(self, index):

        geom = self.geom_index[index]

        match = False
        for group_set in self.groups.values():

            for list_index in group_set:
                list_geom = self.geom_index[list_index]

                dist = shp_distance(geom, list_geom)
                if dist <= self.dist_factor:

                    match = True
                    group_set.add(index)
                    break

            if match:
                break

        if not match:
            self.groups[index].add(index)

    #
    def _merge(self):
        for o_group_key, o_group_set in list(self.groups.items()):

            for i_group_key, i_group_set in list(self.groups.items()):

                if o_group_key == i_group_key:
                    continue

                for o_index in list(o_group_set):
                    o_geom = self.geom_index[o_index]

                    for i_index in list(i_group_set):
                        i_geom = self.geom_index[i_index]

                        dist = shp_distance(o_geom, i_geom)
                        if dist <= self.dist_factor:
                            # do merge
                            if o_group_key in self.groups:
                                print(
                                    o_group_key, i_group_key, o_index, i_index
                                )
                                self.groups[o_group_key] |= self.groups[
                                    i_group_key
                                ]
                                # remove other group
                                del self.groups[i_group_key]

    #
    def export_geoms(self):

        r = defaultdict(list)

        for group_key, group_set in self.groups.items():

            for index in group_set:
                geom = self.geom_index[index]

                r[group_key].append(geom)

        return r
