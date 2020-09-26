"""
    file: optomize.py
    description: Read in a text file pipe separated tweets. Then chronologically sort the time.
                 It will only sort the time stamp. It will not sort by Day or Month or Year.
                 Then it will print out time stamp and its tweet.
    author: La Raw
    date: November 2019
"""

import sys
from timeit import default_timer as timer
import math

class CDLLNode:
    """
        Node Class.
        When it is called it will create a node for Doubly Linked List.
        The Class requires time string, tweet string, [Next node] and [Last node] to instantiate.
            CDLLNode("time","tweet",[Next Node], [Previous Node])

    """
    def __init__(self, time="", tweet="", next_node=None, prev_node=None):
        """
        Constructor for CDLLNode. It creates a node for a Double Linked List.
        :param time: string
        :param tweet: string
        :param next_node: CDLLNode
        :param prev_node: CDLLNode
        """
        self.time: str = time
        self.tweet: str = tweet
        self.next_node: CDLLNode = next_node
        self.prev_node: CDLLNode = prev_node


class CDLL:
    """
        Doubly Linked List. It will contain instances of CDLLNode.
        Upon instantiating it will contain an empty doubly linked list.
    """
    def __init__(self):
        """
            Constructor for CDLL. (Doubly Linked List)
            It contains head  = the smallest time stamp
                        current  = the position of the last search
                                       or the next node position of the newly inserted node.
                        numnodes = the number of nodes that were inserted to the list.
        """

        self.head: CDLLNode = None
        self.current: CDLLNode = None
        self.numnodes: int = 0

    # makes an insertion based on the 'current' node
    def insert(self, time: str, tweet: str) -> None:
        """
        It will insert a new node to the CDLL.
        If it is an empty list, a new node will be inserted and both current and head will point to the node.
        Otherwise, it will insert the node to the left of the current node.
               current previous node <-> new node <-> current node

        :param time: string
                     the time stamp of the tweet
        :param tweet: string
                      the tweet corresponding to the time stamp
        :return: None
                 It will increment the number of nodes contained.
        """
        a_new_node = CDLLNode(time, tweet)

        if self.numnodes == 0:
            self.head = a_new_node
            self.head.next_node = self.head
            self.head.prev_node = self.head
            self.current = self.head

        else:
            a_new_node.next_node = self.current
            a_new_node.prev_node = self.current.prev_node
            self.current.prev_node.next_node = a_new_node
            self.current.prev_node = a_new_node
        self.numnodes += 1

    def go_next(self) -> None:
        """
        Moves 'current' pointer to the next node (circularly)
        :return: None
        :pre: next node of current cannot be NULL
        :post: current pointer is now at the next node ( to right of original position)
        """
        if self.current.next_node is not None:
            self.current = self.current.next_node
            # print("self current go next", self.current.tweet)

    # moves 'current' pointer to the previous node (circularly)
    def go_prev(self):
        """
        Moves 'current' pointer to the previous node (circularly)
        :return: None
        :pre: next node of current cannot be NULL
        :post: current pointer is now at the next node ( to right of original position)
        """
        if self.head:
        # if self.current.prev_node is not None:
            self.current = self.current.prev_node

    # moves 'current' pointer to the head (the first node)
    def go_first(self):
        if self.head:
            self.current = self.head

    # moves 'current' pointer to the last node
    def go_last(self):
        if self.head:
            if self.numnodes > 1:
                self.current = self.head.prev_node

    # moves 'current' pointer n elements ahead (circularly)
    def skip(self, n: int):
        if self.head:
            for i in range(n):
                self.current = self.current.next_node

    # prints the contents of the 'current' node
    # prints the time, then the tweet (each with a newline following)
    def print_current(self):
        if self.head:
            print(self.current.time)
            print(self.current.tweet)

    def get_num_node(self):
        return self.numnodes

    def set_head(self) -> None:
        if self.numnodes >= 2:
            if self.current == self.head:
                head_time = self.head.time
                t_format = "%H:%M:%S"
                # if datetime.strptime(head_time, t_format) >= datetime.strptime(self.current.prev_node.time, t_format):
                if head_time >= self.current.prev_node.time:

                    self.head = self.current.prev_node
                # print(self.head.time)

    def set_current(self, time) -> None:

        if self.numnodes <= 1:
            return

        mid_node_position = math.floor(self.numnodes/2)
        left_node = self.head
        right_node = self.head.prev_node

        left_counter = 0
        right_counter = 0

        self.go_first()

        for i in range (mid_node_position):
            self.current = self.current.next_node

        t_format = "%H:%M:%S"
        # print("while true start")
        while True:
            if left_node.time == time:
                # while
                self.current = left_node
                return
            if self.current.time == time :
                while self.current.prev_node.time == time:
                    self.current = self.current.prev_node
                return
            if right_node.time == time:
                while right_node.prev_node.time  == time:
                    right_node = right_node.prev_node
                self.current = right_node
                return

            # check this one for what it is doing
            if left_node == right_node:
                if left_node.time < time:
                    self.current = left_node.next_node
                    return
                else:
                    self.current = left_node
                    return

            mid_node_position = math.ceil(mid_node_position / 2)

            if self.current.time < time:
                if left_node.time > time:
                    self.current = left_node
                    return
                if right_node.time < time:
                    self.current = right_node.next_node
                    return
                left_node = self.current.next_node
                right_node = right_node.prev_node
                for i in range(mid_node_position):
                    self.current = self.current.next_node
            else:
                if left_node.time > time:
                    self.current = left_node
                    return
                if right_node.time < time:
                    self.current = right_node.next_node
                    return
                right_node = self.current.prev_node
                left_node = left_node.next_node
                for i in range(mid_node_position):
                    self.current = self.current.prev_node

            if left_node.prev_node.time < time and left_node.time > time:
                # while
                self.current = left_node
                return
            if right_node.next_node.time > time and right_node.time < time:
                # while
                self.current = right_node.next_node
                return
            if left_node.next_node == right_node:
                if left_node.time < time:
                    self.current = right_node
                    return
                else:
                    self.current = left_node
                    return

            #mid_node_position =


            # print(self.current.time)


"""End of Class CDLL"""


def print_first_tweet(cdll: CDLL):
    cdll.go_first()
    cdll.print_current()


def print_last_tweet(cdll: CDLL):
    cdll.go_last()
    cdll.print_current()


def print_next_tweet(cdll: CDLL):
    cdll.go_next()
    cdll.print_current()


def print_prev_tweet(cdll: CDLL):
    cdll.go_prev()
    cdll.print_current()


def print_skip_tweet(command: int, cdll: CDLL):
    cdll.skip(command)
    cdll.print_current()


def search_word(command: str, cdll: CDLL):
    cdll.go_next()
    for i in range(cdll.get_num_node()):
        if command in cdll.current.tweet:
            cdll.print_current()
            return
        cdll.current = cdll.current.next_node
    print("Word not found")

def print_num_nodes(cdll: CDLL):
    print(cdll.get_num_node())


def switch_func(command: str, cdll: CDLL) -> None:
    if command.isnumeric():
        num_to_skip = int(command)
    else:
        num_to_skip = 0

    command_dic = {
        "n": print_next_tweet,
        "p": print_last_tweet,
        "f": print_first_tweet,
        "l": print_last_tweet,
        "num": print_num_nodes,
        num_to_skip: print_skip_tweet,
        command: search_word,
    }
    if command is int:
        command_dic.get(num_to_skip)
    else:
        command_dic.get(command)

def bucket_write(arr: CDLL, name: str) -> None:
    orig_stdout = sys.stdout
    with open(name + '.txt', 'w') as name:
        # Make standard output point to our file
        sys.stdout = name
        # Print smiles, which will now be written into the file
        for i in range(arr.get_num_node()):
            arr.print_current()
            arr.go_next()
    # Redirect stdout to our file
    sys.stdout = orig_stdout


def main() -> None:
    """
    The main function
    :return: None
    """
    # START MY TIMER
    start = timer()
    print("read FILE")
    filename = sys.argv[1]
    circular_dll = CDLL()
    # working but taking too long
    with open(filename) as f:
        for line in f:
            data = line.strip().split("|")
            tweet = data[2]
            time = data[1].split()[3]
            circular_dll.set_current(time)
            # circular_dll.print_current()
            # print("finished setting current")
            circular_dll.insert(time, tweet)
            circular_dll.set_head()

    elapsed_time = timer() - start
    print(elapsed_time)
    print("done reading")

    circular_dll.go_first()
    bucket_write(circular_dll,"optimize2")


    user_input = input()
    while user_input != "q":
        # switch_func(user_input, circular_dll)
        if user_input == "n":
            print_next_tweet(circular_dll)
        elif user_input == "p":
            print_prev_tweet(circular_dll)
        elif user_input == "f":
            print_first_tweet(circular_dll)
        elif user_input == "l":
            print_last_tweet(circular_dll)
        elif user_input == "num":
            print(circular_dll.get_num_node())
        elif user_input.isnumeric():
            print_skip_tweet(int(user_input), circular_dll)
        else:
            search_command = user_input.split()
            search_word(search_command[1], circular_dll)
        user_input = input()


if __name__ == "__main__":
    main()
