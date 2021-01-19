#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int average = round((image[i][j].rgbtRed + image[i][j].rgbtGreen + image[i][j].rgbtBlue) / 3.000);
            image[i][j].rgbtRed = average;
            image[i][j].rgbtGreen = average;
            image[i][j].rgbtBlue = average;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int sepiaRed = round(.393 * image[i][j].rgbtRed + .769 * image[i][j].rgbtGreen + .189 * image[i][j].rgbtBlue);
            if (sepiaRed > 255)
            {
                sepiaRed = 255;
            }
            int sepiaGreen = round(.349 * image[i][j].rgbtRed + .686 * image[i][j].rgbtGreen + .168 * image[i][j].rgbtBlue);
            if (sepiaGreen > 255)
            {
                sepiaGreen = 255;
            }
            int sepiaBlue = round(.272 * image[i][j].rgbtRed + .534 * image[i][j].rgbtGreen + .131 * image[i][j].rgbtBlue);
            if (sepiaBlue > 255)
            {
                sepiaBlue = 255;
            }
            image[i][j].rgbtRed = sepiaRed;
            image[i][j].rgbtGreen = sepiaGreen;
            image[i][j].rgbtBlue = sepiaBlue;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width / 2; j++)
        {
            // int tmp[3];
            int tmp0 = image[i][j].rgbtRed;
            int tmp1 = image[i][j].rgbtGreen;
            int tmp2 = image[i][j].rgbtBlue;
            
            image[i][j] = image[i][(width - 1) - j];
            
            image[i][(width - 1) - j].rgbtRed = tmp0;
            image[i][(width - 1) - j].rgbtGreen = tmp1;
            image[i][(width - 1) - j].rgbtBlue = tmp2;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE special[height][width];
    int red;
    int green;
    int blue;
    float number;
    
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            red = 0;
            green = 0;
            blue = 0;
            number = 0.00;
            for (int p = -1; p < 2; p++)
            {
                if (i + p < 0 || i + p > height - 1)
                {
                    continue;
                }
                for (int z = -1; z < 2; z++)
                {
                    if (j + z < 0 || j + z > width - 1)
                    {
                        continue;
                    }
                    red += image[i + p][j + z].rgbtRed;
                    green += image[i + p][j + z].rgbtGreen;
                    blue += image[i + p][j + z].rgbtBlue;
                    number++;
                }
            }
            special[i][j].rgbtRed = round(red / number);
            special[i][j].rgbtGreen = round(green / number);
            special[i][j].rgbtBlue = round(blue / number);
        }
    }
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j].rgbtRed = special[i][j].rgbtRed;
            image[i][j].rgbtGreen = special[i][j].rgbtGreen;
            image[i][j].rgbtBlue = special[i][j].rgbtBlue;
        }
    }
}


