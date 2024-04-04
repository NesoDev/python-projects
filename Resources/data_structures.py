from sorting_algorithms import quickSort


def getIndexMedian(values: list, attribute: str):
    values_sorted = quickSort(values, attribute)
    index_median = [int(len(values_sorted) / 2)]
    if len(values_sorted) % 2 == 0:
        if getattr(values_sorted[index_median[0] - 1], attribute) == getattr(
            values_sorted[index_median[0]], attribute
        ):
            index_median = [index_median[0] - 1, index_median[0]]
    return index_median


class Node:
    def __init__(self):
        self.type = "Node"
        self.data = []
        self.branchLeft = []
        self.branchRight = []

    def setData(self, data: list):
        self.data = data

    def setBranchLeft(self, node: "Node"):
        self.branchLeft = node
        if self.type == "Node":
            self.type = "Leaf"

    def setBranchRight(self, node: "Node"):
        self.branchRight = node
        if self.type == "Node":
            self.type = "Leaf"


class KdBTree:
    def __init__(self, data: list, axis: str, space: int):
        self.root = Node()
        self.fill(data, self.root, axis, 0)
        self.space = space

    def setData(self, data: list):
        self.data = data

    def setRoot(self, root: Node):
        self.root = root

    def getRoot(self):
        return self.root

    def fill(self, data: list, root: Node, axis: str, level: int):

        root.setData(data)

        if len(data) < 2:
            return

        data_sorted = quickSort(data, axis)
        print(f"\ndata_sorted: {[(data.x, data.y) for data in data_sorted]}")
        index_median = getIndexMedian(data_sorted, axis)
        next_axis = "y" if axis == "x" else "x"

        if len(data_sorted) == 2:
            if (
                getattr(data_sorted[1], axis) - getattr(data_sorted[0], axis)
                <= data_sorted[0].radius + data_sorted[1].radius
            ):
                print("Does not separate due to possible collision")
                return
            
        print(f"index: {index_median[0]}")

        data_left = (
            data_sorted[: index_median[0] :] + [data_sorted[i] for i in index_median]
            if len(data_sorted) % 2 == 0 and len(index_median) == 2
            else data_sorted[: index_median[0] :]
        )
        print(f"data_left: {[[d.x, d.y] for d in data_left]}")
        
        data_right = data_sorted[index_median[0] : :]
        print(f"data_right: {[[d.x, d.y] for d in data_right]}")

        node_left = Node()
        node_right = Node()
        root.setBranchLeft(node_left)
        root.setBranchRight(node_right)
        
        self.fill(data_left, root.branchLeft, next_axis, level + 1)
        self.fill(data_right, root.branchRight, next_axis, level + 1)

    def read(self, root: Node):
        print(f"data_node: {[(d.x, d.y) for d in root.data]}")
        if root.branchLeft:
            self.read(root.branchLeft)
        if root.branchRight:
            self.read(root.branchRight)