#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

int main(int argc, char *argv[])
{
    typedef uint8_t BYTE;
    // Incorrect usage
    if (argc != 2)
    {
        printf("Usage: ./recover IMAGE\n");
        return 1;
    }

    // read in file; return 1 if unable to open
    FILE *input = fopen(argv[1], "r");
    if (input == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }


    //JPEG starts with 0xff 0xd8 0xff
    //JPEG end with 0xe0...0xef
    //stored back to back
    //512 byte blocks
    int count = 0;
    BYTE buffer[512];
    char filename[8];
    FILE *img = NULL;

    while (fread(buffer, 1, 512, input) == 512)
    {
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            if (count == 0)
            {
                sprintf(filename, "%03i.jpg", count);
                img = fopen(filename, "w");
                fwrite(buffer, 1, 512, img);
                count++;
            }
            else
            {
                fclose(img);
                sprintf(filename, "%03i.jpg", count);
                img = fopen(filename, "w");
                fwrite(buffer, 1, 512, img);
                count++;
            }
        }
        else
        {
            if (count > 0)
            {
                fwrite(buffer, 1, 512, img);
            }
            else
            {
                continue;
            }
        }
    }
}