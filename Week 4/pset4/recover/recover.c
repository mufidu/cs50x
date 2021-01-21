#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./recover [image name]\n");
        return 1;
    }

    FILE *f = fopen(argv[1], "r");
    if (f == NULL)
    {
        printf("File cannot be opened!\n");
        return 1;
    }

    FILE *img;
    //someone told me the files will be 7
    char filename[7];
    unsigned char *buffer = malloc(512);
    int hitung = 0;

    while (fread(buffer, 512, 1, f))
    {
        //keep reading til a new image discovered
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            //close the previous img (if exist)
            if (hitung >= 1)
            {
                fclose(img);
            }

            //print to the filename
            sprintf(filename, "%03d.jpg", hitung);

            //openn
            img = fopen(filename, "w");

            //check NULL
            if (img == NULL)
            {
                fclose(f);
                printf("Sorry, cant restore the image.");
                free(buffer);
                return 3;
            }

            //else, plus the counter
            hitung++;
        }
        if (hitung >= 1)
        {
            fwrite(buffer, 512, 1, img);
        }
    }

    //free everything n close
    fclose(img);
    fclose(f);
    free(buffer);
    return 0;

}