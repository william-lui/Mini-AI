from __future__ import print_function
from game import sd_peers, sd_spots, sd_domain_num, init_domains, \
    restrict_domain, SD_DIM, SD_SIZE
import random
import copy


class AI:
    def __init__(self):
        pass

    def solve(self, problem):
        # TODO: implement backtracking search.

        # TODO: add any supporting function you need
        domains = init_domains()
        restrict_domain(domains, problem)
        stack = []

        while True:
            if not self.propagate(domains):
                is_consistent = True

                for spot in sd_spots:
                    if len(domains[spot]) != 1:
                        is_consistent = False
                        break

                if is_consistent:
                    return domains

                reset_domain = copy.deepcopy(domains)

                spot, val = self.search(domains)

                stack.append((spot, val, reset_domain))
            else:
                if len(stack) == 0:
                    return None

                domains = self.backtrack(stack, domains)

    def propagate(self, domains):
        is_change = True

        while is_change:
            is_change = False

            for spot in sd_spots:
                if len(domains[spot]) == 1:
                    to_be_remove = domains[spot][0]

                    for neighbor in sd_peers[spot]:
                        if to_be_remove in domains[neighbor]:
                            domains[neighbor].remove(to_be_remove)
                            is_change = True

                            if len(domains[neighbor]) == 0:
                                return True

        return False

    def search(self, domains):
        minimum = SD_SIZE
        unassigned_spot = None
        for spot, val in domains.items():
            if (minimum > len(val) > 1):
                minimum = len(val)
                unassigned_spot = spot

        elt = domains[unassigned_spot][0]

        domains[unassigned_spot] = [elt]
        return unassigned_spot, elt

    def backtrack(self, stack, domains):
        spot, val, reset_domain = stack.pop()
        domains = reset_domain
        domains[spot].remove(val)
        return domains

        #### The following templates are only useful for the EC part #####
        # EC: parses "problem" into a SAT problem
        # of input form to the program 'picoSAT';
        # returns a string usable as input to picoSAT
        # (do not write to file)

    def sat_encode(self, problem):
        text = ""

        # TODO: write CNF specifications to 'text'

        return text

    # EC: takes as input the dictionary mapping
    # from variables to T/F assignments solved for by picoSAT;
    # returns a domain dictionary of the same form
    # as returned by solve()
    def sat_decode(self, assignments):
        # TODO: decode 'assignments' into domains

        # TODO: delete this ->
        domains = {}
        for spot in sd_spots:
            domains[spot] = [1]
        return domains
        # <- TODO: delete this
