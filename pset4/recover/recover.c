#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

typedef uint8_t BYTE;
int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("Usage: Insert File\n");
        return 1;
    }
    
    FILE *file = fopen(argv[1], "r");
    if (!file)
    {
        printf("Insert an apporpriate file format\n");
        return 2;
    }
    
    BYTE bytes[512];
    char nameoffile[8];
    
    FILE *img = NULL;
    int jpegnumber = 0;
    
    while (fread(bytes, 512, 1, file) == 1)
    {
        if (bytes[0] == 0xff && bytes[1] == 0xd8 && bytes[2] == 0xff && (bytes[3] & 0xf0) == 0xe0)
        {
            if (jpegnumber > 0)
            {
                fclose(img);
                sprintf(nameoffile, "%03i.jpg", jpegnumber);
                jpegnumber += 1;
                img = fopen(nameoffile, "w");
                fwrite(bytes, 512, 1, img);
            }
            if (jpegnumber == 0)
            {
                sprintf(nameoffile, "%03i.jpg", jpegnumber);
                jpegnumber += 1;
                img = fopen(nameoffile, "w");
                fwrite(bytes, 512, 1, img);
            }
        }
        else if (jpegnumber > 0)
        {
            fwrite(&bytes, 512, 1, img);
        }
    }
    fclose(img);
    fclose(file);
    return 0;
}
