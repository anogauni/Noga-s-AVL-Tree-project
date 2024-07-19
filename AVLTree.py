

"""A class representing a node in an AVL tree"""

class AVLNode(object):


	"""Constructor, you are allowed to add more fields.

	@type key: int or None
	@param key: key of your node
	@type value: string
	@param value: data of your node
	"""
	def __init__(self, key, value):
		self.key = key
		self.value = value
		self.left = None
		self.right = None
		self.parent = None
		self.height = -1
		self.size = 0
		self.successor_node = None
		self.predecessor_node = None

	""" Returns whether self is not a virtual node 

	@rtype: bool
	@returns: False if self is a virtual node, True otherwise.
	@complexity: O(1)
	"""
	def is_real_node(self):
		if self.key is None and self.value is None:
			return False
		return True

	""" Returns the balance factor of a node
	 @rtype: int
	 @returns: Balance factor of a node
	 @complexity: O(1)
	 """
	def calculate_balance_factor(self):
		if not self.is_real_node():
			return 0
		left_height = self.left.height
		right_height = self.right.height
		return left_height - right_height

	""" Calculates and returns the height of a node
	@rtype: int
	@returns: height of a node
	@post: node's height field not updated within this method
	@complexity: O(1)
	"""
	def check_height(self):
		left_height = self.left.height if self.left else -1
		right_height = self.right.height if self.right else -1
		return max(left_height, right_height) + 1

	""" Calculates and returns the size of the subtree of a node
	@rtype: int
	@returns: size of the subtree of the node, including the node
	@post: node's size field not updated within this method
	@complexity: O(1)
	"""
	def check_size(self):
		if not self.is_real_node():
			return 0
		left_size = self.left.size if self.left.is_real_node() else 0
		right_size = self.right.size if self.right.is_real_node() else 0
		return 1 + left_size + right_size

	""" Method that finds the successor of given node in tree
	@param node: AVLNode to find successor of	
	@return: Successor of given node
	@rtype: AVLNode
	@complexity: O(logn) 
	"""
	def successor(self):
		if self.right.is_real_node():
			return self.find_min_in_subtree(self.right)
		node_y = self.parent
		node_x = self
		while node_y is not None and node_x is node_y.right:
			node_x = node_y
			node_y = node_x.parent

		return node_y

	""" Method that finds the predecessor of given node in tree
	@param self: AVLNode to find predecessor of
	@return predecessor of given AVLNode
	@Complexity: O(logn)
	"""
	def predecessor(self):
		# Case 1: Node has a left child, find the maximum in the left subtree
		if self.left.is_real_node():
			return self.find_max_in_subtree(self.left)

		# Case 2: Node does not have a left child, traverse up the tree
		node_y = self.parent
		node_x = self
		while node_y is not None and node_x is node_y.left:
			node_x = node_y
			node_y = node_x.parent

		return node_y

	""" Method that finds the minimum value in the subtree of the node
	@param node: AVLNode to be searched
	@return: AVLNode with minimum value in the subtree of the node
	@rtype: AVLNode
	@complexity: O(logn)
	"""
	@staticmethod
	def find_min_in_subtree(node):
		while node.left.is_real_node():
			node = node.left
		return node

	""" Method that finds the maximum value in the subtree of the node
	@param node: AVLNode to be searched
	@return: AVLNode with maximum value in the subtree of the node
	@rtype: AVLNode
	@complexity: O(logn)
	"""
	@staticmethod
	def find_max_in_subtree(node):
		while node.right.is_real_node():
			node = node.right
		return node

	""" Function that creates and adds two virtual sons for given node
	@param self: leaf node with no sons 
	@return: None
	@complexity: O(1)
	"""
	def add_virtual_sons(self):
		self.left = AVLNode(None, None)
		self.left.parent = self
		self.right = AVLNode(None, None)
		self.right.parent = self


"""
A class implementing an AVL tree.
"""

class AVLTree(object):

	"""
	Constructor, you are allowed to add more fields.
	@type root: AVLNode Object or None
	@param root: Node to be root of AVLTree
	@complexity: O(1)
	"""
	def __init__(self):
		self.root = AVLNode(None, None)


	"""searches for a node in the dictionary corresponding to the key

	@type key: int
	@param key: a key to be searched
	@rtype: AVLNode
	@returns: node corresponding to key
	@complexity: O(logn)
	"""
	def search(self, key):
		node = self.root
		while node.key != key and node.is_real_node() :
			if node.key > key:
				node = node.left
			elif node.key < key:
				node = node.right
		if node.key == key:
			return node
		return None

	""" Inserts a new node into the dictionary with corresponding key and value
	@type key: int
	@pre: key currently does not appear in the dictionary
	@param key: key of item that is to be inserted to self
	@type val: string
	@param val: the value of the item
	@rtype: int
	@returns: the number of rebalancing operation due to AVL rebalancing
	@post: inserted a new node but did not update parent heights 
	@complexity: O(logn)
	"""
	def insert(self, key, val):

		num_of_operations = 0
		node_y, node_x = None, self.root

		while node_x.is_real_node():
			node_y = node_x
			if key < node_x.key:
				node_x = node_x.left
			else:
				node_x = node_x.right

		#  Arrived at a virtual node
		if node_y is None:  # tree is empty
			self.root.key = key
			self.root.value = val
			self.root.height = 0
			self.root.size = 1
			self.root.add_virtual_sons()
			return num_of_operations

		else:
			node_x.key = key
			node_x.value = val
			node_x.height = 0
			node_x.size = 1
			node_x.add_virtual_sons()

			node_x.successor_node = node_x.successor()
			node_x.predecessor_node = node_x.predecessor()
			if node_x.predecessor_node is not None:
				node_x.predecessor_node.successor_node = node_x
			if node_x.successor_node is not None:
				node_x.successor_node.predecessor_node = node_x


			num_of_operations = self._insertion_fix(node_x.parent)

		return num_of_operations

	""" Method that climbs to root and fixes  AVL Tree
	@pre: new node already added to tree, called from insert method only
	@param node_y: parent AVLNode of inserted node
	@complexity: O(logn)
	"""
	def _insertion_fix(self, node_y):
		number_of_operations = 0
		while node_y is not None:
			original_y_height = node_y.height
			node_y.height = node_y.check_height()
			node_y.size += 1
			bf = node_y.calculate_balance_factor()
			if abs(bf) < 2:
				if original_y_height == node_y.height:
					number_of_operations += self._update_up(node_y.parent)  # update sizes and heights up
					return number_of_operations
				else:
					node_y = node_y.parent
					number_of_operations += 1
			else:  # |bf| = 2
				number_of_operations += self.pick_rotation(node_y)
				number_of_operations += self._update_up(node_y.parent.parent)
				return number_of_operations
		return number_of_operations

	""" Method that climbs to root and fixes size and height of nodes 
	@pre: validated that no rotations are needed from the param node up
	@param node: AVLNode from which to update size and heights of nodes
	@post: updated nodes' size and height fields
	@complexity: O(logn)
	"""
	def _update_up(self, node):
		cnt = 0
		while node is not None:
			original_height = node.height
			node.height = node.check_height()
			if original_height != node.height:
				cnt += 1
			node.size = node.check_size()
			node = node.parent
		return cnt

	""" Deletes a node from the dictionary

	@type node: AVLNode
	@pre: node is a real pointer to a node in self
	@rtype: int
	@returns: the number of rebalancing operation due to AVL rebalancing
	@complexity: O(logn)
	"""
	def delete(self, node):

		if (not (node.left.is_real_node())) and (not (node.right.is_real_node())):  # node is a leaf
			ans = self.delete_leaf(node)
			return ans

		elif (not (node.left.is_real_node())) ^ (not (node.right.is_real_node())):  # node has one child
			ans = self.delete_node_with_one_child(node)

		else:
			ans = self.delete_node_with_two_children(node)

		return ans

	""" Deletes a leaf

		@type node: AVLNode
		@pre: node is a real pointer to a node in self
		@rtype: int
		@returns: the number of rebalancing operation due to AVL rebalancing
		@complexity: O(logn)
		"""
	def delete_leaf(self, node):
		if self.root is node and self.size() == 1:
			self.root = AVLNode(None, None)
			self.root.size = 0
			self.root.height = 0
			return 0
		original_parent = node.parent
		cnt = 0
		if original_parent is not None:
			if original_parent.left is node:
				original_parent.left = AVLNode(None, None)
				original_parent.left.parent = original_parent
			elif original_parent.right is node:
				original_parent.successor_node = original_parent.right.successor_node
				original_parent.right = AVLNode(None, None)
				original_parent.right.parent = original_parent

			if node.predecessor_node is not None:
				node.predecessor_node.successor_node = node.successor_node
			if node.successor_node is not None:
				node.successor_node.predecessor_node = node.predecessor_node

			original_parent.size = original_parent.check_size()

		cnt = self._deletion_fix(original_parent)
		return cnt

	""" Deletes a node with only one child

		@type node: AVLNode
		@pre: node is a real pointer to a node in self
		@rtype: int
		@returns: the number of rebalancing operation due to AVL rebalancing
		@complexity: O(logn)
		"""
	def delete_node_with_one_child(self,node):
		original_parent = node.parent
		cnt = 0
		if original_parent is not None:
			if node.left.is_real_node():  # there is a left son
				if original_parent.left is node:
					original_parent.left = node.left
					node.left.parent = original_parent
				else:
					original_parent.right = node.left
					node.left.parent = original_parent
			else:
				if original_parent.left is node:
					original_parent.left = node.right
					node.right.parent = original_parent
				else:
					original_parent.right = node.right
					node.right.parent = original_parent

			if node.predecessor_node is not None:
				node.predecessor_node.successor_node = node.successor_node
			if node.successor_node is not None:
				node.successor_node.predecessor_node = node.predecessor_node
			original_parent.size = original_parent.check_size()
		else:  # the node is the root with one child
			if node.right.is_real_node():
				node.successor_node.predecessor_node = node.predecessor_node
				self.root = node.right

			else:
				node.predecessor_node.successor_node = node.successor_node
				self.root = node.left
		if original_parent is not None:
			original_parent.size = original_parent.check_size()
		cnt = self._deletion_fix(original_parent)
		return cnt

	""" Deletes a node with two children

		@type node: AVLNode
		@pre: node is a real pointer to a node in self
		@rtype: int
		@returns: the number of rebalancing operation due to AVL rebalancing
		@complexity: O(logn)
		"""
	def delete_node_with_two_children(self, node):  # for node with 2 children, successor has no left child
		original_parent = node.parent
		cnt = 0
		node_succ = node.successor_node
		original_node_successor = node_succ.parent
		if node_succ.height == 0:  # remove successor from the tree: the successor is a leaf or has one right child
			self.delete_leaf(node_succ)
		else:
			self.delete_node_with_one_child(node_succ)

		node_succ.left = node.left  # replacing node by successor: replace its children
		node_succ.right = node.right
		node_succ.left.parent = node_succ
		node_succ.right.parent = node_succ

		node_succ.predecessor_node = node.predecessor_node  # replace succ field
		node_succ.successor_node = node.successor_node

		if node.predecessor_node is not None:
			node_succ.predecessor_node.successor_node = node_succ
		if node.successor_node is not None:
			node_succ.successor_node.predecessor_node = node_succ

		# replace its parent field:
		if node.parent is None:  # in case we delete the root
			node_succ.parent = None
			self.root = node_succ
		else:
			node_succ.parent = node.parent
			if node_succ.parent.left is node:
				node_succ.parent.left = node_succ
			else:
				node_succ.parent.right = node_succ
		node_succ.size = node_succ.check_size()
		cnt = self._deletion_fix(original_parent)
		return cnt

	""" Method that climbs to root and fixes AVL Tree after deletion
	@pre: node already deleted from tree, called from delete method only
	@param node: parent AVLNode of deleted node
	@complexity: O(logn)
	"""
	def _deletion_fix(self, node):
		cnt = 0
		parent = node
		if parent is None:
			original_height = self.root.height
			self.root.height = self.root.check_height()
			self.root.size = self.root.check_size()
			if original_height != self.root.height:
				return 1
			return 0

		while parent is not None:
			original_parent_height = parent.height
			parent.height = parent.check_height()
			parent.size = parent.check_size()
			if original_parent_height != parent.height:  # counting height changes
				cnt += 1
			BF = parent.calculate_balance_factor()  # compute BF of parent
			if abs(BF) < 2 and original_parent_height == parent.height:  # No rotation required
				while parent is not None:
					parent.size = parent.check_size()
					parent = parent.parent
				return cnt
			elif abs(BF) < 2 and original_parent_height != parent.height:  # height changed but BF is ok
				parent = parent.parent  # go back to the while with the parent of the parent, until |BF|=2 found
			else:  # |BF| = 2
				new_parent = parent.parent
				cnt += self.pick_rotation(parent)
				parent = new_parent

		return cnt

	""" Returns an array representing dictionary 
	An envelope function using the function avl_to_array_rec
	@rtype: list
	@returns: a sorted list according to key of tuples (key, value) representing the data structure
	@complexity: O(n)
	"""
	def avl_to_array(self):
		return self.avl_to_array_rec(self.get_root())

	""" Recursive function to return an array representing the dictionary,
	traversing the tree in-order	
	@type node: AVLNode
	@pre: node is a real pointer to a node in self
	@rtype: list
	@returns: a sorted list according to key of touples (key, value)
	"""
	def avl_to_array_rec(self, node):
		if (node is None) or (not node.is_real_node()):
			return []
		return self.avl_to_array_rec(node.left) + [(node.key, node.value)] + self.avl_to_array_rec(node.right)

	"""returns the number of items in dictionary 
	@rtype: int
	@returns: the number of items in dictionary 
	@post: returned integer is full size of the tree including the root
	@complexity: O(1)
	"""
	def size(self):
		if self.root is not None and self.root.is_real_node():
			return self.root.size
		return 0

	""" Computes the rank of node in the dictionary

	@type node: AVLNode
	@pre: node is in self
	@param node: a node in the dictionary to compute the rank for
	@rtype: int
	@returns: the rank of node in self
	@complexity: O(logn)
	"""
	def rank(self, node):
		if not self.root.is_real_node():  # Empty tree
			return 0
		rank_sum = node.left.size + 1
		node_to_check = node
		while node_to_check is not None and node_to_check.parent is not None:
			if node_to_check == node_to_check.parent.right:  # node_to_check is a right son
				rank_sum = rank_sum + node_to_check.parent.left.size + 1
			node_to_check = node_to_check.parent
		return rank_sum

	"""finds the i'th smallest item (according to keys) in the dictionary

	@type i: int
	@pre: 1 <= i <= self.size()
	@param i: the rank to be selected in self
	@rtype: AVLNode
	@returns: the node of rank i in self
	@complexity: O(logn)
	"""
	def select(self, i):
		return self.select_rec(self.root, i)

	"""Recursively searches for the k'th smallest node in the dictionary
	@param node: current AVLNode
	@param k: the index of the node to be searched for
	@rtype: AVLNode
	@returns: the node of rank i in self
	@complexity: O(logn)
	"""
	def select_rec(self, node, k):
		r = node.left.size + 1
		if k == r:
			return node
		elif k < r:
			return self.select_rec(node.left, k)
		else:
			return self.select_rec(node.right, k-r)

	""" Finds node with largest value in a specified range of keys

	@type a: int
	@param a: the lower end of the range
	@type b: int
	@param b: the upper end of the range
	@pre: a<b
	@rtype: AVLNode
	@returns: AVLNode with maximal (lexicographically) value having a<=key<=b, or None if no such keys exist
	@complexity: O(n)
	"""
	def max_range(self, a, b):
		curr_node = self.search(a)  # search the relevant starting point O(logn)
		max_node = curr_node
		while curr_node.is_real_node() and curr_node.key <= b:  # search node with max value. O(n) (if a=min and b=max)
			print(curr_node.key, curr_node.value)
			if curr_node.value.lower() > max_node.value.lower():
				max_node = curr_node

			suc_node = curr_node.successor_node  # O(1)
			curr_node = suc_node
			if curr_node.successor_node is None:
				break

		if max_node.value < curr_node.value:  # if key=b is the largest
			max_node = curr_node

		return max_node

	""" Returns the root of the tree representing the dictionary
	@rtype: AVLNode
	@returns: real pointer to the root, None if the dictionary is empty
	@complexity: O(1)
	"""
	def get_root(self):
		if self.root is not None:
			return self.root
		return None

	""" Function receives a node in the tree where BF has changed to 2 (AVL Criminal) and rotated RR
	@type node: AVLNode
	@param node: AVLNode where BF=2
	@complexity: O(1) 
	"""
	def right_rotation(self, node):
		parent = node.parent
		B = node  # B is original node with BF 2 (root of subtree to rotate)
		A = node.left  # Will be new root of rotated subtree
		B.left = A.right
		B.left.parent = B
		A.parent = parent
		if parent is not None:
			if parent.left == B:
				parent.left = A
			else:
				parent.right = A
		else:
			self.root = A
		A.right = B
		B.parent = A

		A.size = B.size
		B.size = B.check_size()

		B.height = B.check_height()
		A.height = A.check_height()

		return None

	"""Function receives a node in the tree where BF has changed to 2 (AVL Criminal) and rotates LL
	@type node: AVLNode
	@param node: AVLNode where BF=2
	@complexity: O(1)
	
	"""
	def left_rotation(self, node):
		parent = node.parent
		B = node  # B is original node with BF 2 (root of subtree to rotate)
		A = node.right  # Will be new root of rotated subtree
		B.right = A.left
		B.right.parent = B
		A.parent = parent
		if parent is not None:
			if parent.left == B:
				parent.left = A
			else:
				parent.right = A
		else:
			self.root = A
		A.left = B
		B.parent = A

		A.size = B.size
		B.size = B.check_size()

		B.height = B.check_height()
		A.height = A.check_height()
		return None

	""" Function receives a node in the tree where BF has changed to |2| (AVL Criminal) and rotates LR
	@type node: AVLNode
	@param node: AVLNode where BF=2
	@complexity: O(1)
	"""
	def left_then_right_rotation(self, node):
		B = node  # AVL criminal, original node
		parent = B.parent
		A = B.left  # left son of AVL criminal
		C = B.left.right  # node to become new root
		CL = C.left
		CR = C.right

		if parent is None:
			self.root = C
		else:
			if parent.left == B:
				parent.left = C
			else:
				parent.right = C

		C.parent = parent

		C.left = A
		A.parent = C
		C.right = B
		B.parent = C

		A.right = CL
		CL.parent = A
		B.left = CR
		CR.parent = B

		A.size = A.check_size()
		B.size = B.check_size()
		C.size = C.check_size()

		A.height = A.check_height()
		B.height = B.check_height()
		C.height = C.check_height()

		return None

	"""Function receives a node in the tree where BF has changed to 2 (AVL Criminal) and rotates RL
	@type node: AVLNode
	@param node: AVLNode where BF=2
	@complexity: O(1)
	"""
	def right_then_left_rotation(self, node):
		B = node
		parent = B.parent
		A = B.right
		C = B.right.left
		CL = C.right
		CR = C.left

		if parent is None:
			self.root = C
		else:
			if parent.left == B:
				parent.left = C
			else:
				parent.right = C

		C.parent = parent

		C.right = A
		A.parent = C
		C.left = B
		B.parent = C

		A.left = CL
		CL.parent = A
		B.right = CR
		CR.parent = B

		A.size = A.check_size()
		B.size = B.check_size()
		C.size = C.check_size()

		A.height = A.check_height()
		B.height = B.check_height()
		C.height = C.check_height()
		return None

	""" Method that receives a criminal AVLNode and conducts the correct rotation
	@pre: AVL_criminal is indeed a criminal (BF checked and BF = |2|)
	@type AVL_criminal: AVLNode
	@return: None
	@complexcity: O(1)
	"""
	def pick_rotation(self, AVL_criminal):
		criminal_bf = AVL_criminal.calculate_balance_factor()

		if criminal_bf == 2:
			son_bf = AVL_criminal.left.calculate_balance_factor()
			if son_bf == -1:

				self.left_then_right_rotation(AVL_criminal)
				return 2
			else:
				self.right_rotation(AVL_criminal)
				return 1
		else:
			son_bf = AVL_criminal.right.calculate_balance_factor()
			if son_bf == 1:
				self.right_then_left_rotation(AVL_criminal)
				return 2
			else:
				self.left_rotation(AVL_criminal)
				return 1
