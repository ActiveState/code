//file_uniter.cpp
//Unites N files into a single file (or separates them back).
//FB - 201011301
#include<iostream>
#include<fstream>
#include<string>
#include<vector>
using namespace std;

class str
{
    public:
    string s;
    unsigned int l;
};


int main(int argc, char *argv[])
{
    if(argc > 2)
    {
        cerr<<"Too many arguments!"<<endl;
        exit(1);
    }

    unsigned char uc;
    char c;

    if(argc == 2)
    {
        cout<<"File separator mode!"<<endl;

        ifstream infile(argv[1],ios::in|ios::binary);
        if(!infile)
        {
            cerr<<"The file "<<argv[1]<<" could not be opened!"<<endl;
            exit(1);
        }

        string s;
        unsigned int l,j;
        while(true)
        {
            //get the file name
            getline(infile,s);
            if(s.empty())
                break;
            cout<<"file name:"<<s<<endl;
            //get the file length
            //read 4 bytes and combine them into one 32 bit u. int value
            l=0;
            j=1;
            for(int k=3;k>=0;--k)
            {
                infile.get(c);
                uc=c;
                l+=uc*(j<<(8*k));
            }
            cout<<"size:"<<l<<endl;

            ofstream outfile(s.c_str(),ios::out|ios::binary);
            if(!outfile)
            {
                cerr<<"The file "<<s<<" could not be opened!"<<endl;
                exit(1);
            }

            for(unsigned int i=0;i<l;++i)
            {
                infile.get(c);//cout<<c;
                outfile.put(c);
            }
            //cout<<endl;
            outfile.close();
        }
        infile.close();

    }
    else //argc == 1
    {
        cout<<"File uniter mode!"<<endl;

        cout<<"Input the file names! (just Enter to end)"<<endl;
        vector<str> f_names; //file names
        str st;
        while(true)
        {
            getline(cin,st.s);
            if(st.s.empty())
                break;
            ifstream infile(st.s.c_str(),ios::in|ios::binary);
            if(!infile)
            {
                cerr<<"The file "<<st.s<<" could not be opened!"<<endl;
                exit(1);
            }

            //find out the file length (in bytes)
            st.l=0;
            while(infile.get(c))
            {
                ++st.l;
            }
            //cout<<"size:"<<st.l<<endl;
            infile.clear(); //clear the EOF flag
            infile.seekg(0); //reset get() pointer to beginning
            infile.close();

            f_names.push_back(st);
        }

        cout<<"Input the output file name:"<<endl;
        string s;
        cin>>s;
        ofstream outfile(s.c_str(), ios::out|ios::binary);
        if(!outfile)
        {
            cerr<<"The file "<<s<<" could not be opened!"<<endl;
            exit(1);
        }
        
        //output file format: filename1, filelength1, file1, ...
        for(unsigned int i=0;i<f_names.size();++i)
        {
            outfile.write(f_names.at(i).s.c_str(),f_names.at(i).s.size());
            //add a next line char to the end of the file name
            c='\n';
            uc=c;
            outfile.put(uc);

            //write the file length
            //divide 32 bit u. int values into 4 bytes
            outfile.put(static_cast<unsigned char>(f_names.at(i).l>>24));
            outfile.put(static_cast<unsigned char>((f_names.at(i).l>>16)%256));
            outfile.put(static_cast<unsigned char>((f_names.at(i).l>>8)%256));
            outfile.put(static_cast<unsigned char>(f_names.at(i).l%256));

            //write the file 
            ifstream infile(f_names.at(i).s.c_str(),ios::in|ios::binary);
            for(unsigned int j=0;j<f_names.at(i).l;++j)
            {
                infile.get(c);
                outfile.put(c);
            }
            infile.clear(); //clear the EOF flag
            infile.seekg(0); //reset get() pointer to beginning
            infile.close();
        }            

    }//end else

    return 0;
}
