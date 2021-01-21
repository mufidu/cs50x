#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    float gray;

    for (int i = 0; i < width; i++)
    {
        for (int j = 0; j < height; j++)
        {
            gray = round((image[j][i].rgbtBlue + image[j][i].rgbtRed + image[j][i].rgbtGreen) / 3.00);
            image[j][i].rgbtBlue = gray;
            image[j][i].rgbtRed = gray;
            image[j][i].rgbtGreen = gray;
        }
    }
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    int sepiaRed;
    int sepiaGreen;
    int sepiaBlue;
    for (int i = 0; i < width; i++)
    {
        for (int j = 0; j < height; j++)
        {
            sepiaRed = round(0.393 * image[j][i].rgbtRed + 0.769 * image[j][i].rgbtGreen + 0.189 * image[j][i].rgbtBlue);
            sepiaGreen = round(0.349 * image[j][i].rgbtRed + 0.686 * image[j][i].rgbtGreen + 0.168 * image[j][i].rgbtBlue);
            sepiaBlue = round(0.272 * image[j][i].rgbtRed + 0.534 * image[j][i].rgbtGreen + 0.131 * image[j][i].rgbtBlue);

            if (sepiaRed > 255)
            {
                sepiaRed = 255;
            }
            if (sepiaGreen > 255)
            {
                sepiaGreen = 255;
            }
            if (sepiaBlue > 255)
            {
                sepiaBlue = 255;
            }

            image[j][i].rgbtRed = sepiaRed;
            image[j][i].rgbtGreen = sepiaGreen;
            image[j][i].rgbtBlue = sepiaBlue;
        }
    }
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    //declare the temp for storing things
    int tmp[3];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            //start swapping
            tmp[0] = image[j][i].rgbtRed;
            tmp[1] = image[j][i].rgbtGreen;
            tmp[2] = image[j][i].rgbtBlue;

            //swap again
            image[j][i].rgbtRed = image[j][width - i - 1].rgbtRed;
            image[j][i].rgbtGreen = image[j][width - i - 1].rgbtGreen;
            image[j][i].rgbtBlue = image[j][width - i - 1].rgbtBlue;

            //last swap I promise :)
            image[j][width - i - 1].rgbtRed = tmp[0];
            image[j][width - i - 1].rgbtGreen = tmp[1];
            image[j][width - i - 1].rgbtBlue = tmp[2];
        }
    }
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    int Red;
    int Green;
    int Blue;
    float hitung;
    RGBTRIPLE tmp[height][width];

    for (int i = 0; i < width; i++)
    {
        for (int j = 0; j < height; j++)
        {
            Blue = 0;
            Green = 0;
            Red = 0;
            hitung = 0.00;

            for (int k = -1; k < 2; k++)
            {
                if (j + k < 0 || j + k > height - 1)
                {
                    continue;
                }

                for (int h = -1; h < 2; h++)
                {
                    if (i + h < 0 || i + h > width - 1)
                    {
                        continue;
                    }
                    
                    Red += image[j + k][i + h].rgbtRed;
                    Green += image[j + k][i + h].rgbtGreen;
                    Blue += image[j + k][i + h].rgbtBlue;
                    
                    hitung++;
                }
            }

            // averages the sum to make picture look blurrier
            tmp[j][i].rgbtRed = round(Red / hitung);
            tmp[j][i].rgbtGreen = round(Green / hitung);
            tmp[j][i].rgbtBlue = round(Blue / hitung);
        }
    }
    for (int i = 0; i < width; i++)
    {
        for (int j = 0; j < height; j++)
        {
            image[j][i].rgbtBlue = tmp[j][i].rgbtBlue;
            image[j][i].rgbtGreen = tmp[j][i].rgbtGreen;
            image[j][i].rgbtRed = tmp[j][i].rgbtRed;
        }
    }
}
