// sfrender: render a note list through a SoundFont to a 48 kHz stereo 16-bit WAV.
// Usage: sfrender <soundfont.sf2> <notes.txt> <out.wav> <seconds>
// notes.txt lines: start_s dur_s channel bank program key velocity(0..1)   (channel 0..15)
// Built on TinySoundFont (MIT, Bernhard Schelling). Part of 805 Score Lab's score pipeline.
#define TSF_IMPLEMENTATION
#include "tsf.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
typedef struct { double t; int on; int ch; int bank; int prog; int key; float vel; } Ev;
static int cmp(const void*a,const void*b){double d=((Ev*)a)->t-((Ev*)b)->t; if(d<0)return -1; if(d>0)return 1; return ((Ev*)a)->on-((Ev*)b)->on;}
int main(int argc,char**argv){
  if(argc<5){fprintf(stderr,"usage\n");return 1;}
  tsf* f=tsf_load_filename(argv[1]); if(!f){fprintf(stderr,"cannot load sf2\n");return 1;}
  const int SR=48000; tsf_set_output(f,TSF_STEREO_INTERLEAVED,SR,-6.0f);
  tsf_channel_set_bank_preset(f,9,128,0);
  FILE*in=fopen(argv[2],"r"); int cap=1<<16,n=0; Ev*ev=malloc(sizeof(Ev)*cap);
  double s,d; int ch,bank,prog,key; float vel;
  while(fscanf(in,"%lf %lf %d %d %d %d %f",&s,&d,&ch,&bank,&prog,&key,&vel)==7){
    if(n+2>=cap){cap*=2;ev=realloc(ev,sizeof(Ev)*cap);}
    ev[n++]=(Ev){s,1,ch,bank,prog,key,vel}; ev[n++]=(Ev){s+d,0,ch,bank,prog,key,0};
  }
  fclose(in); qsort(ev,n,sizeof(Ev),cmp);
  long total=(long)(atof(argv[4])*SR); short*buf=malloc(sizeof(short)*2*total); long pos=0; int i=0;
  int setprog[16]; for(int c=0;c<16;c++) setprog[c]=-1;
  while(pos<total){
    while(i<n && (long)(ev[i].t*SR)<=pos){
      Ev e=ev[i++];
      if(e.on){ int id=e.bank*1000+e.prog; if(setprog[e.ch]!=id){tsf_channel_set_bank_preset(f,e.ch,e.bank,e.prog); setprog[e.ch]=id;}
                tsf_channel_note_on(f,e.ch,e.key,e.vel);} else tsf_channel_note_off(f,e.ch,e.key);
    }
    long next=(i<n)?(long)(ev[i].t*SR):total; if(next>total) next=total; long blk=next-pos; if(blk>4096) blk=4096; if(blk<1) blk=1;
    tsf_render_short(f,buf+2*pos,(int)blk,0); pos+=blk;
  }
  FILE*o=fopen(argv[3],"wb"); int dsz=total*4; int hdr[11];
  fwrite("RIFF",1,4,o); int v=36+dsz; fwrite(&v,4,1,o); fwrite("WAVEfmt ",1,8,o); v=16; fwrite(&v,4,1,o);
  short fmt[2]={1,2}; fwrite(fmt,2,2,o); v=SR; fwrite(&v,4,1,o); v=SR*4; fwrite(&v,4,1,o); short ba[2]={4,16}; fwrite(ba,2,2,o);
  fwrite("data",1,4,o); fwrite(&dsz,4,1,o); fwrite(buf,2,2*total,o); fclose(o); (void)hdr;
  return 0;
}
