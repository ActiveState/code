//huffman.cpp
//Huffman Encoding (Data Compression)
//Compiler used: Dev-C++ 4.9.9.2
//FB - 201011301

#include<iostream>
#include<fstream>
#include<string>
#include<iomanip> //for width()
#include<cctype> //for sprintf()

#define HELP_ERROR 99
#define width_unit 5

using namespace std;

// (Templated d-heap) (on dynamic array of pointers)
// priority queue
// min (root=min) ((balanced) d-tree on dynamic array) d-heap
template<class T>
class Queue
{
    public:

        Queue(int d=2); //constructor 
        ~Queue(void); //destructor
        void enq(T*); //enqueue (to push)
        T* deq(void); //dequeue (to pop)
        T* front(void); //the front element
        bool empty(void) const; //is empty?
        bool full(void) const; //is full?

    private:

        int back; //the last element in the queue
        T* *arr; //dynamic array
        int size; //current size of the queue array
        static const int SIZE=10; //size increment step size  
        int D; //max number of children for a parent>=2 
        //copy constructor and assignment are hidden to protect 
        Queue(const Queue &);
        const Queue & operator=(const Queue &);

        //utility functions to fix the heap
        //when an element added or removed 
        void reheapup(int, int); //fix heap upward
        void reheapdown(int, int); //fix heap downward
        void swap(T* &, T* &); //swap f. needed by reheapup/down functions

}; //end class


// constructor (creates a new queue) 
template<class T>
Queue<T>::Queue(int d)
{
    if(d<2) d=2; //min a 2-heap is supported
    D=d;
    back=0;
    size=SIZE;
    arr=new T*[size];
}

// is queue empty?
template<class T>
bool Queue<T>::empty(void) const
{
    return (back<=0);
}

// is queue full?
template<class T>
bool Queue<T>::full(void) const
{
    return (back>=size);
}

// the front element of the queue 
template<class T>
T* Queue<T>::deq(void)
{
    if(empty())
    {
        cerr<<"deq error! exiting..."<<endl;
        exit(1);
    }

    T* rval=arr[0];
    arr[0]=arr[back-1]; //the element in the back moved to front
    --back;
    reheapdown(0, back-1); //reheapdown called to fix the order back 
    return rval;
}

// a copy of the front element is returned but the queue is not changed
template<class T>
T* Queue<T>::front(void)
{
    if(empty())
    {
        cerr<<"deq error! exiting..."<<endl;
        exit(1);
    }

    return arr[0];
}

// a new element to put in the queue
template<class T>
void Queue<T>::enq(T* foo)
{
    if(full()) //if the array is full then make it larger
    {
        int nsize=size+SIZE; //the size of the new array
        T* *narr=new T*[nsize]; //new array
        for(int i=0;i<size;++i) //copy old array to the new one
            narr[i]=arr[i];
        delete[] arr; //delete reserved old array mem
        arr=narr; //pointer update
        size=nsize; //size update
    }

    //the new element added to the back of the queue
    //and the reheapup called to fix the order back
    arr[back++]=foo; //arr[back]=foo;++back;
    reheapup(0, back-1); 
}

// this is a recursive function to fix back the order in the queue
// upwards after a new element added back (bottom) of the queue 
template<class T>
void Queue<T>::reheapup(int root, int bottom)
{
    int parent; //parent node (in the virtual tree) of the bottom element

    if(bottom > root)
    {
        parent=(bottom-1)/D;

        //compare the two node and if the order is wrong then swap them
        //and make a recursive call to continue upward in the virtual tree
        //until the whole tree heap order is restored   
        if(*arr[parent] > *arr[bottom])
        {
            swap(arr[parent], arr[bottom]);
            reheapup(root, parent);
        }
    }
}

// this is a recursive function to fix back the order in the queue
// downwards after a new element added front (root) of the queue 
template<class T>
void Queue<T>::reheapdown(int root, int bottom)
{
    int minchild, firstchild, child;

    firstchild=root*D+1; //the position of the first child of the root

    if(firstchild <= bottom) //if the child is in the queue
    {
        minchild=firstchild; //first child is the min child (temporarily)

        for(int i=2;i <= D;++i)
        {
            child=root*D+i; //position of the next child
            if(child <= bottom) //if the child is in the queue
            {
                //if the child is less than the current min child
                //then it will be the new min child
                if(*arr[child] < *arr[minchild])
                {
                    minchild=child;
                }
            }
        }

        //if the min child found is less then the root(parent node)
        //then swap them and call reheapdown() recursively and
        //continue to fix the order in the virtual tree downwards
        if(*arr[root] > *arr[minchild])
        {
            swap(arr[root], arr[minchild]);
            reheapdown(minchild, bottom);
        }
    } 
}

// the values of 2 variables will be swapped
template<class T>
void Queue<T>::swap(T* &a, T* &b)
{
    T* c;
    c=a;
    a=b;
    b=c;
}

// destructor (because default dest. does not erase the array)
template<class T>
Queue<T>::~Queue(void)
{
    delete[] arr;
}


// Huffman Tree
class Tree
{
    private:
        class Node
        {
            public:
                unsigned int freq;
                unsigned char ch;
                Node *left, *right;
                //constructor
                Node(void)
                    :freq(0), ch('\0'), left(NULL), right(NULL) {}
        };

        Node *root;

        //copy cons. and assign. op. overload prototypes are private to
        //prevent them to be used
        Tree(const Tree &); //copy constructor
        const Tree & operator=(const Tree &); //assignment oper. overload
        void chop(Node * N); //destroys the tree
        void print(ostream &, Node *, int) const; //prints the tree
        void print(Node *, int) const; //prints the tree

    public:
        Tree(void); //constructor
        ~Tree(void); //destructor
        friend ostream & operator<<(ostream &, const Tree &);
        //utility functions to get or set class members
        unsigned int get_freq(void) const;
        unsigned char get_char(void) const;
        void set_freq(unsigned int);
        void set_char(unsigned char);
        Node* get_left(void) const;
        Node* get_right(void) const;
        void set_left(Node *);
        void set_right(Node *);
        Node* get_root(void) const;
        //comparison operator overloads to compare
        //2 objects of the class
        bool operator==(const Tree &) const;
        bool operator!=(const Tree &) const;
        bool operator<(const Tree &) const;
        bool operator>(const Tree &) const;
        bool operator<=(const Tree &) const;
        bool operator>=(const Tree &) const;

        //to get H. string of a given char
        void huf(Node *, unsigned char, string, string &) const; 
        //outputs the H. char-string pairs list
        void huf_list(Node *, string) const; 
        //to get char equivalent of a H. string (if exists)
        bool get_huf_char(string, unsigned char &) const;
        string print_char(Node *) const; //prints chars 
};

//constructor
Tree::Tree(void)
{
    Node* N=new Node;
    root=N;
}

//recursive func to delete the whole tree
void Tree::chop(Node *N)
{
    if(N)
    {
        chop(N->left);
        chop(N->right);
        delete N;
    }
}

//destructor for tree objects
Tree::~Tree(void)
{
    chop(root);
}

unsigned int Tree::get_freq(void) const
{
    return root->freq;
}

unsigned char Tree::get_char(void) const
{
    return root->ch;
}

void Tree::set_freq(unsigned int f)
{
    root->freq=f;
}

void Tree::set_char(unsigned char c)
{
    root->ch=c;
}

Tree::Node* Tree::get_left(void) const
{
    return root->left;
}

Tree::Node* Tree::get_right(void) const
{
    return root->right;
}

void Tree::set_left(Node* N)
{
    root->left=N;
}

void Tree::set_right(Node* N)
{
    root->right=N;
}

Tree::Node* Tree::get_root(void) const
{
    return root;
}

//the recursive tree output (w/ respect to its graph) fn.
void Tree::print(ostream & ost, Node * curr, int level) const
{
    if(curr) //if the current node is not null then
    {
        print(ost,curr->right,level+1); //try to go to right node
        //output the node data w/ respect to its level
        ost<<setw(level*width_unit)<<print_char(curr)<<":"
           <<curr->freq<<endl;
        print(ost,curr->left,level+1); //try to go to left node
    }
}

//the recursive tree print (w/ respect to its graph) fn.
void Tree::print(Node * curr, int level) const
{
    if(curr) //if the current node is not null then
    {
        print(curr->right,level+1); //try to go to right node
        //print the node data w/ respect to its level
        cout<<setw(level*width_unit)<<print_char(curr)<<":"
            <<curr->freq<<endl;
        print(curr->left,level+1); //try to go to left node
    }
}

//utility fn to output a tree
ostream & operator<<(ostream &ost, const Tree &t)
{
    t.print(ost, t.root, 1);
    return ost;
}

//the comparison operator overloads to compare 2 Huffman trees

bool Tree::operator==(const Tree & T) const
{
    return (root->freq == T.root->freq);    
}

bool Tree::operator!=(const Tree & T) const
{
    return (root->freq != T.root->freq);    
}

bool Tree::operator<(const Tree & T) const
{
    return (root->freq < T.root->freq);    
}

bool Tree::operator>(const Tree & T) const
{
    return (root->freq > T.root->freq);    
}

bool Tree::operator<=(const Tree & T) const
{
    return (root->freq <= T.root->freq);    
}

bool Tree::operator>=(const Tree & T) const
{
    return (root->freq >= T.root->freq);    
}

//Huffman string finder (recursive func.)
//input : a tree node to start the search, a char to find its
//        Huffman string equivalent, current Huffman string according to
//        position on the Huffman tree, and a string (by reference) to
//        copy the resulted full Huffman string end of the search
//return: none (except Huffman string by reference)
void Tree::huf(Node* N, unsigned char c, string str, string & s) const
{
    if(N) //if the node is not null
    {
        //compare char of the leaf node and the given char
        if(!N->left && !N->right && N->ch == c)
        {
            s=str; //if the char is found then copy the H. string
        }
        else
        {
            //continue to search if the same char still not found
            huf(N->left, c, str+"0",s);
            huf(N->right, c, str+"1",s);
        }
    }
}

//Huffman char-string lister (recursive func.)
//input : a tree node to start the search, current Huffman string according to
//        position on the Huffman tree
//output: whole list of char-H. string code list of the H. tree
void Tree::huf_list(Node* N, string str) const
{
    if(N) //if the node is not null
    {
        if(!N->left && !N->right) //if it is a leaf node
            cout<<print_char(N)<<" "<<str<<endl;
        else
        {
            //continue to search
            huf_list(N->left, str+"0");
            huf_list(N->right, str+"1");
        }
    }
}

//char finder with given Huffman string
//input : a Huffman string to traverse on the H. tree and
//        a u. char by ref. to copy the char found
//return: true if a char is found else false
bool Tree::get_huf_char(string s, unsigned char & c) const
{
    Node * curr=root;
    for(unsigned int i=0;i<s.size();++i)
    {
        if(s[i]=='0') //go to left in the H. tree
            curr=curr->left;
        if(s[i]=='1') //go to right in the H. tree
            curr=curr->right;
    }

    bool found=false;

    if(!curr->left && !curr->right) //if it is a leaf node
    {
        found=true;
        c=curr->ch;
    }

    return found;
}

//input : a H. tree node
//return: the same char as string or if the char is not printable
//        then its octal representation in the ASCII char set
string Tree::print_char(Node * N) const
{
    string s="";

    if(!N->left && !N->right) //if it is a leaf node
    {
        unsigned char c=N->ch;

        //if the char is not printable then output its octal ASCII code
        if(iscntrl(c) || c==32) //32:blank char
        {
            //calculate the octal code of the char (3 digits)
            char* cp=new char;
            for(int i=0;i<3;++i)
            {
                sprintf(cp,"%i",c%8);
                c-=c%8;
                c/=8;
                s=(*cp)+s;
            }
            s='/'+s; // adds \ in front of the octal code
        }
        else
            s=c;
    }
    return s;
}

//the given bit will be written to the output file stream
//input : unsigned char i(:0 or 1 : bit to write ; 2:EOF) 
void huf_write(unsigned char i, ofstream & outfile)
{
    static int bit_pos=0; //0 to 7 (left to right) on the byte block
    static unsigned char c='\0'; //byte block to write

    if(i<2) //if not EOF
    {
        if(i==1)
            c=c | (i<<(7-bit_pos)); //add a 1 to the byte
        else //i==0
            c=c & static_cast<unsigned char>(255-(1<<(7-bit_pos))); //add a 0
        ++bit_pos;
        bit_pos%=8;
        if(bit_pos==0)
        {
            outfile.put(c);
            c='\0';
        }
    }
    else
    {
        outfile.put(c);
    }
}

//input : a input file stream to read bits
//return: unsigned char (:0 or 1 as bit read or 2 as EOF) 
unsigned char huf_read(ifstream & infile)
{
    static int bit_pos=0; //0 to 7 (left to right) on the byte block
    static unsigned char c=infile.get();

    unsigned char i;

    i=(c>>(7-bit_pos))%2; //get the bit from the byte
    ++bit_pos;
    bit_pos%=8;
    if(bit_pos==0)
        if(!infile.eof())
        {
            c=infile.get();
        }
        else
            i=2;

    return i;     
}

//Huffman Encoder
void encoder(string ifile, string ofile, bool verbose)
{
    ifstream infile(ifile.c_str(), ios::in|ios::binary);
    if(!infile)
    {
        cerr<<ifile<<" could not be opened!"<<endl;
        exit(1);
    }

    if(ifstream(ofile.c_str()))
    {
        cerr<<ofile<<" already exists!"<<endl;
        exit(1);
    }

    //open the output file
    ofstream outfile(ofile.c_str(), ios::out|ios::binary);
    if(!outfile)
    {
        cerr<<ofile<<" could not be opened!"<<endl;
        exit(1);
    }

    //array to hold frequency table for all ASCII characters in the file
    unsigned int f[256];
    for(int i=0;i<256;++i)
        f[i]=0;

    //read the whole file and count the ASCII char table frequencies
    char c;
    unsigned char ch;
    while(infile.get(c))
    {
        ch=c;
        ++f[ch];
    }

    infile.clear(); //clear EOF flag
    infile.seekg(0); //reset get() pointer to beginning

    Queue<Tree> q(3); //use a 3-(priority)heap
    Tree* tp;

    for(int i=0;i<256;++i)
    {
        //output char freq table to the output file
        //divide 32 bit u. int values into 4 bytes
        outfile.put(static_cast<unsigned char>(f[i]>>24));
        outfile.put(static_cast<unsigned char>((f[i]>>16)%256));
        outfile.put(static_cast<unsigned char>((f[i]>>8)%256));
        outfile.put(static_cast<unsigned char>(f[i]%256));
 
        if(f[i]>0)
        {
            //send freq-char pairs to the priority heap as Huffman trees
            tp=new Tree;
            (*tp).set_freq(f[i]);
            (*tp).set_char(static_cast<unsigned char>(i));
            q.enq(tp);
        }
    }

    //construct the main Huffman Tree
    Tree* tp2;
    Tree* tp3;

    do
    {
        tp=q.deq();
        if(!q.empty())
        {
            //get the 2 lowest freq. H. trees and combine them into one
            //and put back into the priority heap
            tp2=q.deq();
            tp3=new Tree;
            (*tp3).set_freq((*tp).get_freq()+(*tp2).get_freq());
            (*tp3).set_left((*tp).get_root());
            (*tp3).set_right((*tp2).get_root());
            q.enq(tp3);
        }
    }
    while(!q.empty()); //until all sub-trees combined into one

    //find H. strings of all chars in the H. tree and put into a string table
    string H_table[256];
    unsigned char uc;
    for(unsigned short us=0;us<256;++us)
    {
        H_table[us]="";
        uc=static_cast<unsigned char>(us);
        (*tp).huf((*tp).get_root(), uc, "", H_table[us]);
    } 

    if(verbose)
    {
        cout<<*tp<<endl; //output the Huffman tree
        //output the char-H. string list 
        (*tp).huf_list((*tp).get_root(), "");
        cout<<"frequency table is "<<sizeof(unsigned int)*256<<" bytes"<<endl;
    }

    unsigned int total_chars=(*tp).get_freq();
    cout<<"total chars to encode:"<<total_chars<<endl;

    //output Huffman coded chars into the output file
    unsigned char ch2;
    while(infile.get(c))
    {
        ch=c;
        //send the Huffman string to output file bit by bit
        for(unsigned int i=0;i<H_table[ch].size();++i)
        {
            if(H_table[ch].at(i)=='0')
                ch2=0;
            if(H_table[ch].at(i)=='1')
                ch2=1;
            huf_write(ch2, outfile);
        }
    }
    ch2=2; // send EOF
    huf_write(ch2, outfile);

    infile.close();
    outfile.close();

} //end of Huffman encoder

//Huffman Decoder
void decoder(string ifile, string ofile, bool verbose)
{
    ifstream infile(ifile.c_str(), ios::in|ios::binary);
    if(!infile)
    {
        cerr<<ifile<<" could not be opened!"<<endl;
        exit(1);
    }

    if(ifstream(ofile.c_str()))
    {
        cerr<<ofile<<" already exists!"<<endl;
        exit(1);
    }

    //open the output file
    ofstream outfile(ofile.c_str(), ios::out|ios::binary);
    if(!outfile)
    {
        cerr<<ofile<<" could not be opened!"<<endl;
        exit(1);
    }

    //read frequency table from the input file
    unsigned int f[256];
    char c;
    unsigned char ch;
    unsigned int j=1;
    for(int i=0;i<256;++i)
    {
        //read 4 bytes and combine them into one 32 bit u. int value
        f[i]=0;
        for(int k=3;k>=0;--k)
        {
            infile.get(c);
            ch=c;
            f[i]+=ch*(j<<(8*k));
        }
    }

    //re-construct the Huffman tree
    Queue<Tree> q(3); //use a 3-(priority)heap (again)
    Tree* tp;

    for(int i=0;i<256;++i)
    {
        if(f[i]>0)
        {
            //send freq-char pairs to the priority heap as Huffman trees
            tp=new Tree;
            (*tp).set_freq(f[i]);
            (*tp).set_char(static_cast<unsigned char>(i));
            q.enq(tp);
        }
    }

    //construct the main Huffman Tree (as in Encoder func.)
    Tree* tp2;
    Tree* tp3;

    do
    {
        tp=q.deq();
        if(!q.empty())
        {
            //get the 2 lowest freq. H. trees and combine them into one
            //and put back into the priority heap
            tp2=q.deq();
            tp3=new Tree;
            (*tp3).set_freq((*tp).get_freq()+(*tp2).get_freq());
            (*tp3).set_left((*tp).get_root());
            (*tp3).set_right((*tp2).get_root());
            q.enq(tp3);
        }
    }
    while(!q.empty()); //until all sub-trees combined into one

    if(verbose)
    {
        cout<<*tp<<endl; //output the Huffman tree
        //output the char-H. string list 
        (*tp).huf_list((*tp).get_root(), "");
        cout<<"frequency table is "<<sizeof(unsigned int)*256<<" bytes"<<endl;
    }

    //read Huffman strings from the input file
    //find out the chars and write into the output file
    string st;
    unsigned char ch2;
    unsigned int total_chars=(*tp).get_freq();
    cout<<"total chars to decode:"<<total_chars<<endl;
    while(total_chars>0) //continue until no char left to decode 
    {
        st=""; //current Huffman string
        do
        {
            //read H. strings bit by bit
            ch=huf_read(infile);
            if(ch==0)
                st=st+'0';
            if(ch==1)
                st=st+'1';
        } //search the H. tree
        while(!(*tp).get_huf_char(st, ch2)); //continue until a char is found

        //output the char to the output file
        outfile.put(static_cast<char>(ch2));
        --total_chars;
    }

    infile.close();
    outfile.close();

} //end of Huffman decoder

void usage_msg ( const string & pname )
{
    cerr << "Usage: " << pname << " : valid flags are :" << endl
        << " -i input_file  : required" << endl
        << " -o output_file : required" << endl
        << " -e  : turn on encoding mode ( default )" << endl
        << " -d  : turn on decoding mode" << endl
        << " -v  : verbose mode" << endl
        << " -h  : this help screen" << endl;
}

int main( int argc, char * argv[] )
{
    string in_name;
    string out_name;
    bool encode = true;
    bool verbose = false;

    for ( int i = 1 ; i < argc ; ++i )
    {
        if ( !strcmp( "-h", argv[i] ) || !strcmp( "--help", argv[i] ) )
        {
            usage_msg( argv[0] );
            exit( HELP_ERROR );
        }
        else if ( !strcmp( "-i", argv[i] ) )
        {
            cerr << "input file is '" << argv[++i] << "'" << endl;
            in_name = argv[i];
        }
        else if ( !strcmp( "-o", argv[i] ) )
        {
            cerr << "output file is '" << argv[++i] << "'" << endl;
            out_name = argv[i];
        }
        else if ( !strcmp( "-d", argv[i] ) )
        {
            encode = false;
        }
        else if ( !strcmp( "-e", argv[i] ) )
        {
            encode = true;
        }
        else if ( !strcmp( "-v", argv[i] ) )
        {
            verbose = true;
        }

    }
    if ( !in_name.size() || !out_name.size() )
    {
        cerr << "input and output file are required, nothing to do!" << endl;
        usage_msg( argv[0] );
        exit( HELP_ERROR );
    }

    if ( encode )
    {
        cerr << "running in encoder mode" << endl;
        encoder( in_name, out_name, verbose );
    }
    else
    {
        cerr << "running in decoder mode" << endl;
        decoder( in_name, out_name, verbose );
    }
    cerr << "done .... " << endl;

    return 0;
}
