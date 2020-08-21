#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>

int main(int argc, char *argv[])
{
    // Check for command line argument
    if (argc != 2)
    {
        fprintf(stderr, "Usage: recover infile\n");
        return 1;
    }

    // Open file
    FILE *file = fopen(argv[1], "r");

    // Check there is data on file
    if (file == NULL)
    {
        fprintf(stderr, "Could not open %s\n", argv[1]);
        return 1;
    }

    // Create image file
    FILE *image = NULL;

    // Set 512 byte array and filename array, and set counter
    unsigned char buffer[512];
    int counter = 0;
    char filename[8];
    
    // Set jpeg bool
    bool isJpeg = false;

    // Read each block
    while (fread(buffer, 512, 1, file) == 1)
    {
        // Find out if jpeg
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            // Close current image if is jpeg
            if (isJpeg == true)
            {
                fclose(image);
            }
            
            // Found jpeg
            else 
            {
                isJpeg = true;
            }
            
            // Print file name and open new image
            sprintf(filename, "%03i.jpg", counter);
            image = fopen(filename, "w");
            counter++;
        }
         
        // Continue writing if block is still jpeg
        if (isJpeg == true)
        {
            fwrite(buffer, 512, 1, image);
        }
    }
    
    // Close files
    fclose(file);
    fclose(image);

    // Success
    return 0;
}
