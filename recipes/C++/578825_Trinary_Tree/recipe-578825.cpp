/*
 *
 * Implement insert and delete in a tri-nary tree
 *
 */


#include <iostream>

// data structure of Tri-Nary tree node
struct TreeNode {
  int val;
  TreeNode *left;
  TreeNode *middle;
  TreeNode *right;
  TreeNode(int value):
    val(value), left(NULL), middle(NULL), right(NULL) {}
};

// data structure of Tri-Nary tree
class Tri_Nary_Tree {
  private:
    TreeNode *root;
    void insertNode(TreeNode *node, int value);
    TreeNode* deleteNode(TreeNode *node, int value);
    TreeNode* findSuccessor(TreeNode *node);
  public:
    Tri_Nary_Tree():root(NULL) {}
    void insertNode(int value);
    void deleteNode(int value);
};

void Tri_Nary_Tree::insertNode(int value) {
  if (root == NULL)
    root = new TreeNode(value);
  else
    insertNode(root, value);
}

void Tri_Nary_Tree::insertNode(TreeNode *node, int value) {
  if (node->val < value) {
    if (node->right)
      insertNode(node->right, value);
    else
      node->right = new TreeNode(value);
  }
  else if (node->val > value) {
    if (node->left)
      insertNode(node->left, value);
    else
      node->left = new TreeNode(value);
  }
  else {
    if (node->middle)
      insertNode(node->middle, value);
    else
      node->middle = new TreeNode(value);
  }
}

inline void Tri_Nary_Tree::deleteNode(int value) {
  root = deleteNode(root, value);
}

TreeNode* Tri_Nary_Tree::deleteNode(TreeNode *node, int value) {

  if (node == NULL)
    return node;

  if (node->val == value) {
    // three child nodes are all NULL
    if (node->left == NULL && node->right == NULL && node->middle == NULL) {
      delete node;
      return NULL;
    }
    if (node->middle) {
      node->middle = deleteNode(node->middle, value);
    }
    else {
      if (node->left && node->right) {  // both left and right exist
        TreeNode *successor_node = findSuccessor(node->right);
        node->val = successor_node->val;
        node->right = deleteNode(node->right, successor_node->val);
      }
      else if (node->left) {    // right child is empty
        TreeNode *new_node = node->left;
        delete node;
        return new_node;
      }
      else {                   // left child is empty
        TreeNode *new_node = node->right;
        delete node;
        return new_node;
      }
    }
  }
  else if (node->val < value)
    node->right = deleteNode(node->right, value);
  else
    node->left = deleteNode(node->left, value);

  return node;
}

// find the successor (in inorder traversal) in right child
TreeNode* Tri_Nary_Tree::findSuccessor(TreeNode *node) {
  if (node->left == NULL)
    return node;
  else
    return findSuccessor(node->left);
}
