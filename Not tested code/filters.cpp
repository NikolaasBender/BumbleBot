#include<iostream.h>
#include<conio.h>
#include<math.h>



//=========================================================
//JUST THE STRUCTURE FOR EACH PIXEL
//=========================================================
struct pixel(){
	int r = 0;
	int g = 0;
	int b = 0;
}



//=========================================================
//WRITE THE BMP
//=========================================================
Save1BppImage(byte* ImageData, const char* filename, long w, long h){

    int bitmap_dx = 1280; // Width of image
    int bitmap_dy = 720; // Height of Image

    // create file
    std::ofstream file(filename, std::ios::binary | std::ios::trunc);
    if(!file) return;

    // save bitmap file headers
    BITMAPFILEHEADER fileHeader;
    BITMAPINFOHEADER * infoHeader;
    infoHeader = (BITMAPINFOHEADER*) malloc(sizeof(BITMAPINFOHEADER) );
    RGBQUAD bl = {0,0,0,0};  //black color
    RGBQUAD wh = {0xff,0xff,0xff,0xff}; // white color


    fileHeader.bfType      = 0x4d42;
    fileHeader.bfSize      = 0;
    fileHeader.bfReserved1 = 0;
    fileHeader.bfReserved2 = 0;
    fileHeader.bfOffBits   = sizeof(BITMAPFILEHEADER) + (sizeof(BITMAPINFOHEADER));

    infoHeader->biSize          = (sizeof(BITMAPINFOHEADER) );
    infoHeader->biWidth         = bitmap_dx;    
    infoHeader->biHeight        = bitmap_dy;
    infoHeader->biPlanes        = 1;
    infoHeader->biBitCount      = 1;
    infoHeader->biCompression   = BI_RGB; //no compression needed
    infoHeader->biSizeImage     = 0;
    infoHeader->biXPelsPerMeter = 0;
    infoHeader->biYPelsPerMeter = 0;
    infoHeader->biClrUsed       = 2;
    infoHeader->biClrImportant  = 2;

    file.write((char*)&fileHeader, sizeof(fileHeader)); //write bitmapfileheader
    file.write((char*)infoHeader, (sizeof(BITMAPINFOHEADER) )); //write bitmapinfoheader
    file.write((char*)&bl,sizeof(bl)); //write RGBQUAD for black
    file.write((char*)&wh,sizeof(wh)); //write RGBQUAD for white

    int bytes = (w/8) * h ; //for example for 32X64 image = (32/8)bytes X 64 = 256;

    file.write((const char*)ImageData, bytes);

    file.close();
}






//=========================================================
//READ THE BMP
//=========================================================
unsigned char* readBMP(char* filename)
{
    int i;
    FILE* f = fopen(filename, "rb");
    unsigned char info[54];
    fread(info, sizeof(unsigned char), 54, f); // read the 54-byte header

    // extract image height and width from header
    int width = *(int*)&info[18];
    int height = *(int*)&info[22];

    int size = 3 * width * height;
    unsigned char* data = new unsigned char[size]; // allocate 3 bytes per pixel
    fread(data, sizeof(unsigned char), size, f); // read the rest of the data at once
    fclose(f);

    for(i = 0; i < size; i += 3)
    {
            unsigned char tmp = data[i];
            data[i] = data[i+2];
            data[i+2] = tmp;
    }

    return data;
}



//=========================================================
//=========================================================
//MAIN
//=========================================================
//=========================================================
int main(){
	
	


	for(int w = 0; w < 1280; w++){
		for(int h = 0; h < 720; h++){
			pixel tmp = pic[w][h];
			int norm = pow(pow(tmp -> r,2) + pow(tmp -> g,2) + pow(tmp -> b,2),0.5);
			picBW[w][h] = norm;
		}
	}
	
}