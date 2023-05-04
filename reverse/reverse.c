#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#include "wav.h"

int check_format(WAVHEADER header);
int get_block_size(WAVHEADER header);

int main(int argc, char *argv[])
{
    // Ensure proper usage
    if (argc != 3)
    {
        printf("Usage: ./reverse input.wav output.wav\n");
        return 1;
    }

    // Open input file for reading
    FILE *input = fopen(argv[1], "rb");

    if (input == NULL)
    {
        printf("Could not open file\n");
        return 1;
    }

    // Read header
    WAVHEADER header;
    fread(&header, sizeof(WAVHEADER), 1, input);

    // Use check_format to ensure WAV format
    if (!check_format(header))
    {
        fclose(input);
        printf("Input is not a WAV file.\n");
        return 1;
    }

    // Open output file for writing
    FILE *output = fopen(argv[2], "wb");

    if (output == NULL)
    {
        fclose(input);
        printf("Could not open file");
        return 1;
    }

    // Write header to file
    fwrite(&header, sizeof(WAVHEADER), 1, output);

    // Use get_block_size to calculate size of block
    int block_size = get_block_size(header);

    // Write reversed audio to file
    fseek(input, 0L, SEEK_END); // Set the file position indicator to the end of the input file
    long size = ftell(input) - sizeof(WAVHEADER); // Get the size of the input file in bytes
    fseek(input, 0L, SEEK_SET); // Set the file position indicator back to the beginning of the input file

    unsigned char buffer[block_size];

    for (long i = size - block_size; i >= 0; i -= block_size)
    {
        fseek(input, i + sizeof(WAVHEADER), SEEK_SET);
        fread(&buffer, sizeof(unsigned char), block_size, input);
        fwrite(&buffer, sizeof(unsigned char), block_size, output);
    }

    fclose(input);
    fclose(output);
}

int check_format(WAVHEADER header)
{
    int checker = 0;

    char true_format[] = {'W', 'A', 'V', 'E'};
    for (int i = 0; i < 4; i++)
    {
        if (header.format[i] == (BYTE) true_format[i])
        {
            checker++;
        }
    }

    if (checker == 4)
    {
        return 1;
    }

    return 0;
}

int get_block_size(WAVHEADER header)
{
    return header.numChannels * header.bitsPerSample / 8;
}