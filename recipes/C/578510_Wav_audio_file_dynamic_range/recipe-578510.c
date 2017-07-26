#include <stdio.h>
/*
gcc -o autolvl4.out autolvl4.c;./autolvl4.out
*/

// Auto-adjust the gain to keep a fairly constant volume.

#define g_numsamples 11000 // Min 12000 ok 
#define g_max_clip_level 32767
#define d_max_ampl 5000.0 // 4000 -> -17dB, 5000 -> -15dB, 5500 -> -14dB

char g_input[] = "seesound.wav";
char g_output[100] = {0};
double gain_ceiling=5.0;

short signed int scale_data(short signed int data, double gain)
{
	short signed int n_result=0;
	double d_result=(double)data * gain;
	if (d_result < -32768.0) 
	{
		d_result = -32768.0;
	}
	if (d_result > 32767.0)
	{
		d_result = 32767.0;
	}
	n_result = (short signed int)d_result;
	return n_result;
}

double abs_scale_data(short signed int data, double gain)
{
	double d_result=(double)data * gain;
	if (d_result<0.0) d_result=-d_result;
	return d_result;
}


int main(void)
{
	FILE *fin;
	long i=0;
	long j=0;

	double sumL=0.0;
	double sumR=0.0;
	double count=0.0;

	g_output[0] = '0';
	g_output[1] = '_';
	for (i=0; i<99; i++)
	{
		g_output[i+2]=g_input[i];
	}

	double locgainl=0.0;
	double locgainr=0.0;
	long loccount=0;

	short signed int ndata[g_numsamples]={0};
	short signed int cheader[88]={0};
	char b_make_output=0;
	long num_blocks=0;

	long num_gains=0;
	double l_gains[40000]={0.0};
	double r_gains[40000]={0.0};

	double l_avg_gains[40000]={0.0};
	double r_avg_gains[40000]={0.0};

	fin=fopen(g_input,"rb");
	if (!fin) 
	{
		printf("Error opening input file\n");
		return 0;
	}
	else
	{
		printf("Opening %s\n", g_input);
	}
	fseek(fin,88,SEEK_SET);

/*_____________________________


		MAIN LOOP

_____________________________*/

	double dgains[2]={0.0};
	long int gainptr=0;
	while(1)
	{
		if (feof(fin)) break;
		num_blocks++;
		fread(ndata,sizeof(ndata),1,fin);
		i=0;
		long int j=0;
		locgainl=0.0;
		locgainr=0.0;
		loccount=0;
		for (i=0;i<g_numsamples;i++)
			if (ndata[i]<0) ndata[i]=-ndata[i];
		for (i=0;i<g_numsamples;i+=2)
		{
			sumL+=(double)ndata[i];
			sumR+=(double)ndata[i+1];
			locgainl+=(double)ndata[i];
			locgainr+=(double)ndata[i+1];
			count+=1.0;
			loccount++;
		}
		// calculate the average
		locgainl/=(double)loccount;
		locgainr/=(double)loccount;

		// scale the average to meet the gain.
		locgainl=d_max_ampl/locgainl;
		locgainr=d_max_ampl/locgainr;
		dgains[0]=locgainl;
		dgains[1]=locgainr;

		if (locgainl > gain_ceiling) locgainl = gain_ceiling;
		if (locgainr > gain_ceiling) locgainr = gain_ceiling;

		l_gains[gainptr]=locgainl;
		r_gains[gainptr]=locgainr;
		gainptr++;
	}
	num_gains=gainptr;

	sumL/=count;
	sumR/=count;

/*__________________________________________


		Make sure that no interval clips or
		exceeds the gain specification.

____________________________________________*/

	fseek(fin,0,SEEK_SET);
	gainptr=0;
	double locdatal=0.0;
	double locdatar=0.0;
	double maxlocdata=0.0;
	while(1)
	{
		if (feof(fin)) break;
		fread(ndata,sizeof(ndata),1,fin);
		i=0;
		long int j=0;
		maxlocdata=0;
		for (i=0;i<g_numsamples;i++)
			if (ndata[i]<0) ndata[i]=-ndata[i];
		for (i=0;i<g_numsamples;i+=2)
		{
			locdatal=abs_scale_data(ndata[i],   l_gains[gainptr]);
			locdatar=abs_scale_data(ndata[i+1], r_gains[gainptr]);
			if (locdatal > maxlocdata) maxlocdata = locdatal;
			if (locdatar > maxlocdata) maxlocdata = locdatar;
		}

		if (maxlocdata >= g_max_clip_level)
		{
			double factor=g_max_clip_level / maxlocdata;
			l_gains[gainptr] *= factor;
			r_gains[gainptr] *= factor;
		}
		gainptr++;
	}

	// l_avg_gains
	long llim=0;
	long ulim=0;

	for (i=0; i<num_gains; i++)
	{
		double dlavg=0.0;
		double dravg=0.0;
		long j=0;
		double dcount=0.0;
		llim=i-10;
		ulim=i+10;
		dlavg=0.0;
		dravg=0.0;
		if (llim < 0)
		{
			llim=0;
			ulim-=llim;
		}
		for (j=llim; j<ulim; j++)
		{
			dlavg+=l_gains[j];
			dravg+=r_gains[j];
			dcount+=1.0;
		}
		dlavg/=dcount;
		dravg/=dcount;
		l_avg_gains[i]=dlavg;
		r_avg_gains[i]=dravg;
	}


	for (i=0; i<num_gains; i++)
	{
		double dfactor=0.0;
		double dnewgain=0.0;

		if (l_gains[i] > l_avg_gains[i])
		{
			dfactor=l_gains[i]/l_avg_gains[i];
			dnewgain=(l_gains[i] * dfactor) + l_avg_gains[i];
			dnewgain /= (dfactor + 1);
			l_gains[i] = dnewgain;
		}

		if (r_gains[i] > r_avg_gains[i])
		{
			dfactor=r_gains[i]/r_avg_gains[i];
			dnewgain=(r_gains[i] * dfactor) + r_avg_gains[i];
			dnewgain /= (dfactor + 1);
			r_gains[i] = dnewgain;
		}
	}

	// Make it so that the gains can decrease rapidly, but not increase as fast.
	// If a future gain is a lot bigger than a previous gain, then scale it back.

	for (i=1; i<num_gains; i++)
	{
		if (l_gains[i]>l_gains[i-1])
		{
			l_gains[i]=(l_gains[i]+l_gains[i-1]*3.0)/4.0;
		}
		if (r_gains[i]>r_gains[i-1])
		{
			r_gains[i]=(r_gains[i]+r_gains[i-1]*3.0)/4.0;
		}
	}

	long block=0;
	double d_ldata=0.0;
	double d_rdata=0.0;
	double lgain=0.0;
	double rgain=0.0;

/*_____________________________________


		Do the dynamic compression here

_______________________________________*/

	i=0;
	printf("Auto-scale volume\n");
	lgain=d_max_ampl/sumL;
	rgain=d_max_ampl/sumR;

	double lgaininc=0.0;
	double rgaininc=0.0;
	double dlastgains[2] = {0.0};

	double lptgain=0.0;
	double rptgain=0.0;

	double dpercent_in_file=0.0;

	FILE *fout;
	fout=fopen(g_output,"wb");
	if (fout)
	{
		fseek(fin,0,SEEK_SET);
		fread(cheader,sizeof(cheader),1,fin);
		fwrite(cheader,sizeof(cheader),1,fout);

		gainptr=0;
		dgains[0]=l_gains[gainptr];
		dgains[1]=r_gains[gainptr++];

		for (block=0; block<num_blocks; block++)
		{
			fread(ndata,sizeof(ndata),1,fin);

			// leave the dynamics at the end alone.
			// could make this a percentage too.
			// when we are 97% of the way through the song,
			// just let it ride out and don't adjust the gain
			// from what it was.

			dpercent_in_file = (double)block / (double)num_blocks;

			if (dpercent_in_file < 0.97)
			{
				dlastgains[0]=dgains[0];
				dlastgains[1]=dgains[1];

				lptgain=dlastgains[0];
				rptgain=dlastgains[1];

				if (lptgain > gain_ceiling) lptgain = gain_ceiling;
				if (rptgain > gain_ceiling) rptgain = gain_ceiling;

				dgains[0]=l_gains[gainptr];
				dgains[1]=r_gains[gainptr++];

				lgaininc=(dgains[0]-dlastgains[0]) / (double)g_numsamples;
				rgaininc=(dgains[1]-dlastgains[1]) / (double)g_numsamples;
			}
			else 
			{
				lgaininc=0;
				rgaininc=0;
			}

			long i=0;
			for (i=0;i<g_numsamples;i+=2)
			{
				ndata[i]   = scale_data(ndata[i]  , lptgain);
				ndata[i+1] = scale_data(ndata[i+1], rptgain);

				lptgain += lgaininc;
				rptgain += rgaininc;
			}

			fwrite(ndata,sizeof(ndata),1,fout);
		}

		while(1)
		{
			if (feof(fin)) break;
			fread(ndata,sizeof(short signed int),1,fin);
			short int i=0;
			ndata[i]=scale_data(ndata[i], lgain);
			ndata[i+1]=scale_data(ndata[i+1], rgain);
			fwrite(ndata,sizeof(short signed int),1,fout);
		}

		fclose(fout);
	}
	else
	{
		printf("Error opening output file\n");
	}

	printf("lgain = %.2f\n", lgain);
	printf("rgain = %.2f\n", rgain);
	
	fclose(fin);

	return 0;
}
