#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int ii = 0; ii < width; ii++)
        {
            int gray = round((image[i][ii].rgbtRed + image[i][ii].rgbtGreen + image[i][ii].rgbtBlue) / 3.0);

            image[i][ii].rgbtRed = gray;
            image[i][ii].rgbtGreen = gray;
            image[i][ii].rgbtBlue = gray;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int ii = 0; ii < width; ii++)
        {
            int originalRed = image[i][ii].rgbtRed;
            int originalGreen = image[i][ii].rgbtGreen;
            int originalBlue = image[i][ii].rgbtBlue;

            int sepiaRed = round((.393 * originalRed) + (.769 * originalGreen) + (.189 * originalBlue));
            int sepiaGreen = round((.349 * originalRed) + (.686 * originalGreen) + (.168 * originalBlue));
            int sepiaBlue = round((.272 * originalRed) + (.534 * originalGreen) + (.131 * originalBlue));

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

            image[i][ii].rgbtRed = sepiaRed;
            image[i][ii].rgbtGreen = sepiaGreen;
            image[i][ii].rgbtBlue = sepiaBlue;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE tmp;
    for (int i = 0; i < height; i++)
    {
        for (int ii = 0; ii < width / 2; ii++)
        {
            tmp = image[i][(width - 1) - ii];
            image[i][(width - 1) - ii] = image[i][ii];
            image[i][ii] = tmp;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE copy[height][width];

    // create copy of image
    for (int i = 0; i < height; i++)
    {
        for (int ii = 0; ii < width; ii++)
        {
            copy[i][ii] = image[i][ii];
        }
    }

    // take avg of each rgb from copy pixel
    for (int i = 0; i < height; i++)
    {
        for (int ii = 0; ii < width; ii++)
        {
            float avgRed = copy[i][ii].rgbtRed;
            float avgGreen = copy[i][ii].rgbtGreen;
            float avgBlue = copy[i][ii].rgbtBlue;
            float count = 1;

            //right
            if (ii != width - 1)
            {
                count++;
                avgRed += copy[i][ii + 1].rgbtRed;
                avgGreen += copy[i][ii + 1].rgbtGreen;
                avgBlue += copy[i][ii + 1].rgbtBlue;
            }

            if (ii != 0)
            {
                //left
                count++;
                avgRed += copy[i][ii - 1].rgbtRed;
                avgGreen += copy[i][ii - 1].rgbtGreen;
                avgBlue += copy[i][ii - 1].rgbtBlue;
            }

            if (i != 0)
            {
                //above
                count++;
                avgRed += copy[i - 1][ii].rgbtRed;
                avgGreen += copy[i - 1][ii].rgbtGreen;
                avgBlue += copy[i - 1][ii].rgbtBlue;
            }

            if (i != height - 1)
            {
                //below
                count++;
                avgRed += copy[i + 1][ii].rgbtRed;
                avgGreen += copy[i + 1][ii].rgbtGreen;
                avgBlue += copy[i + 1][ii].rgbtBlue;
            }

            if ((i != 0) && (ii != 0))
            {
                //upper left
                count++;
                avgRed += copy[i - 1][ii - 1].rgbtRed;
                avgGreen += copy[i - 1][ii - 1].rgbtGreen;
                avgBlue += copy[i - 1][ii - 1].rgbtBlue;
            }

            if ((i != height - 1) && (ii != 0))
            {
                //lower left
                count++;
                avgRed += copy[i + 1][ii - 1].rgbtRed;
                avgGreen += copy[i + 1][ii - 1].rgbtGreen;
                avgBlue += copy[i + 1][ii - 1].rgbtBlue;
            }

            if ((i != 0) && (ii != width - 1))
            {
                //upper right
                count++;
                avgRed += copy[i - 1][ii + 1].rgbtRed;
                avgGreen += copy[i - 1][ii + 1].rgbtGreen;
                avgBlue += copy[i - 1][ii + 1].rgbtBlue;
            }

            if ((i != height - 1) && (ii != width - 1))
            {
                //lower right
                count++;
                avgRed += copy[i + 1][ii + 1].rgbtRed;
                avgGreen += copy[i + 1][ii + 1].rgbtGreen;
                avgBlue += copy[i + 1][ii + 1].rgbtBlue;
            }

            avgRed = round(avgRed / count);
            avgGreen = round(avgGreen / count);
            avgBlue = round(avgBlue / count);

            // set avg rbg values in image pixel
            image[i][ii].rgbtRed = avgRed;
            image[i][ii].rgbtGreen = avgGreen;
            image[i][ii].rgbtBlue = avgBlue;
        }
    }
    return;
}
