#include "helpers.h"
#include <stdio.h>
#include <math.h>
#include <string.h>
#include <stdlib.h>

void average(int i, int j, int top, int bottom, int left, int right, int h, int w, RGBTRIPLE image[h][w], RGBTRIPLE temp[h][w]);
void copy(int height, int width, RGBTRIPLE im1[height][width], RGBTRIPLE im2[height][width]);
void add_border(int height, int width, RGBTRIPLE image[height][width]);
void sobel_operator(int i, int j, int h, int w, RGBTRIPLE image[h][w], RGBTRIPLE temp[h+2][w+2]);
float* calculate_g(int i, int j, int weights[3][3], int h, int w, RGBTRIPLE image[h][w]);

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    float sum;
    float avg;
    int rounded_avg;

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            sum = image[i][j].rgbtBlue + image[i][j].rgbtGreen + image[i][j].rgbtRed;
            avg = sum / 3.0;
            rounded_avg = (uint8_t) roundf(avg);

            image[i][j].rgbtBlue = rounded_avg;
            image[i][j].rgbtGreen = rounded_avg;
            image[i][j].rgbtRed = rounded_avg;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE temprow[height][width];

    copy(height, width, image, temprow);

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j] = temprow[i][width - 1 - j];
        }
    }

    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE temp[height][width];

    copy(height, width, image, temp);

    average(0, 0, 0, 1, 0, 1, height, width, image, temp);
    average(0, width - 1, 0, 1, 1, 0, height, width, image, temp);
    average(height - 1, 0, 1, 0, 0, 1, height, width, image, temp);
    average(height - 1, width - 1, 1, 0, 1, 0, height, width, image, temp);

    for (int i = 1; i < height - 1; i++)
    {
        for (int j = 1; j < width - 1; j++)
        {
            average(i, j, 1, 1, 1, 1, height, width, image, temp);
            average(0, j, 0, 1, 1, 1, height, width, image, temp);
            average(height - 1, j, 1, 0, 1, 1, height, width, image, temp);
        }

        average(i, 0, 1, 1, 0, 1, height, width, image, temp);
        average(i, width - 1, 1, 1, 1, 0, height, width, image, temp);
    }

    copy(height, width, temp, image);

    return;
}

void average(int i, int j, int top, int bottom, int left, int right, int h, int w, RGBTRIPLE image[h][w], RGBTRIPLE temp[h][w])
{
    float sum[] = {0, 0, 0};
    float avg[3];
    int rounded_avg[3];
    int count = 0;

    for (int k = i - top; k <= i + bottom; k++)
    {
        for (int l = j - left; l <= j + right; l++)
        {
            sum[0] += image[k][l].rgbtBlue;
            sum[1] += image[k][l].rgbtGreen;
            sum[2] += image[k][l].rgbtRed;

            count++;
        }
    }

    for (int k = 0; k < 3; k++)
    {
        avg[k] = (float)sum[k] / count;
        rounded_avg[k] = (uint8_t) roundf(avg[k]);
    }

    temp[i][j].rgbtBlue = rounded_avg[0];
    temp[i][j].rgbtGreen = rounded_avg[1];
    temp[i][j].rgbtRed = rounded_avg[2];

    return;
}

void copy(int height, int width, RGBTRIPLE im1[height][width], RGBTRIPLE im2[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for ( int j = 0; j < width; j++)
        {
            im2[i][j] = im1[i][j];
        }
    }

    return;
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE temp[height + 2][width + 2];

    add_border(height + 2, width + 2, temp);

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            temp[i + 1][j + 1] = image[i][j];
        }
    }

    for (int i = 1; i < height + 1; i++)
    {
        for (int j = 1; j < width + 1; j++)
        {
            sobel_operator(i, j, height, width, image, temp);
        }
    }

    return;
}

void add_border(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        image[i][0].rgbtBlue = 0;
        image[i][0].rgbtGreen = 0;
        image[i][0].rgbtRed = 0;

        image[i][width - 1].rgbtBlue = 0;
        image[i][width - 1].rgbtGreen = 0;
        image[i][width - 1].rgbtRed = 0;
    }

    for (int i = 0; i < width; i++)
    {
        image[0][i].rgbtBlue = 0;
        image[0][i].rgbtGreen = 0;
        image[0][i].rgbtRed = 0;

        image[height - 1][i].rgbtBlue = 0;
        image[height - 1][i].rgbtGreen = 0;
        image[height - 1][i].rgbtRed = 0;
    }

    return;
}

void sobel_operator(int i, int j, int h, int w, RGBTRIPLE image[h][w], RGBTRIPLE temp[h+2][w+2])
{
    int xweights[3][3] = {{-1, 0, 1}, {-2, 0, 2}, {-1, 0, 1}};
    int yweights[3][3] = {{-1, -2, -1}, {0, 0, 0}, {1, 2, 1}};

    float* gx = calculate_g(i, j, xweights, h + 2, w + 2, temp);
    float* gy = calculate_g(i, j, yweights, h + 2, w + 2, temp);

    int combi[3];
    uint8_t comb[3];

    for (int k = 0; k < 3; k++)
    {
        combi[k] = roundf(sqrt(gx[k] * gx[k] + gy[k] * gy[k]));
        if (combi[k] > 255)
        {
            combi[k] = 255;
        }
        comb[k] = (uint8_t) combi[k];
    }

    image[i - 1][j - 1].rgbtBlue = comb[0];
    image[i - 1][j - 1].rgbtGreen = comb[1];
    image[i - 1][j - 1].rgbtRed = comb[2];

    return;
}

float* calculate_g(int i, int j, int weights[3][3], int h, int w, RGBTRIPLE temp[h][w])
{
    float* sum = (float*) malloc(3 * sizeof(float));

    for (int k = 0; k < 3; k++)
    {
        sum[k] = 0;
    }

    for (int k = 0; k < 3; k++)
    {
        for (int l = 0; l < 3; l++)
        {
            sum[0] += temp[k + i - 1][l + j - 1].rgbtBlue * weights[k][l];
            sum[1] += temp[k + i - 1][l + j - 1].rgbtGreen * weights[k][l];
            sum[2] += temp[k + i - 1][l + j - 1].rgbtRed * weights[k][l];
        }
    }

    return sum;
}