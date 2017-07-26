#include <iostream>
#include <sstream>
#include <vector>
#include <algorithm>
#include <pngwriter.h>



using namespace std;
using std::vector;


#define HEIGHT 528
#define WIDTH 528
#define DEPTH 5
#define SLICE 3
#define MULT 3

string volume_data = "/home/zahari/Desktop/brainDATAsmall.vol";
string output_image = "mri.png";





void Tokenize(const string& str,
                      vector<string>& tokens,
                      const string& delimiters = " ")
{
    // Skip delimiters at beginning.
    string::size_type lastPos = str.find_first_not_of(delimiters, 0);
    // Find first "non-delimiter".
    string::size_type pos     = str.find_first_of(delimiters, lastPos);

    while (string::npos != pos || string::npos != lastPos)
    {
        // Found a token, add it to the vector.
        tokens.push_back(str.substr(lastPos, pos - lastPos));
        // Skip delimiters.  Note the "not_of"
        lastPos = str.find_first_not_of(delimiters, pos);
        // Find next "non-delimiter"
        pos = str.find_first_of(delimiters, lastPos);
    }
}



int main() {
	
	
	FILE *fp;
	long len;
	char *buf;
	fp=fopen(volume_data.c_str(),"rb");
	fseek(fp,0,SEEK_END); //go to end
	len=ftell(fp); //get position at end (length)
	fseek(fp,0,SEEK_SET); //go to beg.
	buf=(char *)malloc(len); //malloc buffer
	fread(buf,len,1,fp); //read into buffer
	fclose(fp);

	double dens_value;
	int X_index;
	int Y_index;
	int Z_index;
	cout.precision(15);
	int xcounter;
	int ycounter;
	pngwriter png(HEIGHT,WIDTH,0,output_image.c_str());
    
    
    /////////////////////////////////////////
    
    
    vector<vector<vector<double> > > array3D;

  
  array3D.resize(HEIGHT);
  for (int i = 0; i < HEIGHT; ++i) {
    array3D[i].resize(WIDTH);

    for (int j = 0; j < WIDTH; ++j)
      array3D[i][j].resize(DEPTH);
  }

  

    
    
    ///////////////////////////////////////
    
    

	
	
	
     
   std::string initial_string;
   std::vector<string> int_list;
   Tokenize(buf,int_list,";");
   
   
   std::vector<string> vallist;

   for (vector<string>::iterator i = int_list.begin();
                           i != int_list.end() - 1;
                           ++i)
{
	

    initial_string = *i;

    vector<string> tokens;

   Tokenize(initial_string, tokens);
     
           for (vector<string>::iterator i = tokens.begin();
          	  
                            i != tokens.end();
                            ++i) 
           {
           cout<< *i <<"  ";
          	   }
          	  dens_value = strtod(tokens[3].c_str(),NULL);
          	  X_index = atoi(tokens[0].c_str());
          	  Y_index = atoi(tokens[1].c_str());
          	  Z_index = atoi(tokens[2].c_str());
          	  array3D[X_index][Y_index][Z_index] = dens_value * MULT;
          	  
          	  cout<< " " <<"X: "<< X_index <<
                    " " <<"Y: "<< Y_index <<
          	          " " <<"Z: "<< Z_index <<
          	          " " <<"Value:"<< dens_value <<
          	          " " <<"               Array Value:"<< array3D[X_index][Y_index][Z_index] <<endl;

          	          
          	          
          	          
}


   for(ycounter = 1; ycounter < HEIGHT;ycounter++)
     {
     	     for(xcounter = 1; xcounter < WIDTH;xcounter++)
     	     {
     	             png.plot(xcounter,-1, 
     	             	      array3D[xcounter][ycounter][SLICE], 
     	             	      array3D[xcounter][ycounter][SLICE], 
     	             	      array3D[xcounter][ycounter][SLICE]);

     	
             }
     }

png.close();


cout << "---::::::: " << HEIGHT*WIDTH*DEPTH << " :::::::---  processed." << endl;
return 0;
}
