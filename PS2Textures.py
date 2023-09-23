
# UnSwizzle PS2 Textures
# https://github.com/leeao/PS2Textures

'''
How to UnSwizzle:
    4bpp type 1:
        rrw = width // 2
        rrh = height // 4
        PSMCT32Buffer = writeTexPSMCT32(0, rrw // 64, 0, 0, rrw, rrh, pixelBuffer)
        pixel = readTexPSMT4(0, width // 64, 0, 0, width, height, PSMCT32Buffer) 

    4bpp type 2:
        Method 1:
            pixelBuffer = unswizzle4(pixelBuffer, width, height)
    
        Method 2: Convert 4bpp to 8bpp
            pixelBuffer = convert4bppto8bpp(pixelBuffer, width, height)
            rrw = width // 2
            rrh = height // 2        
            PSMCT32Buffer = writeTexPSMCT32(0, rrw // 64, 0, 0, rrw, rrh, pixelBuffer)
            unswizzleBuffer = readTexPSMT8(0, width // 64, 0, 0, width, height, PSMCT32Buffer) 

    8bpp:
        Method 1:
            pixelBuffer = unswizzle8(buffer, width, height)
            
        Method 2:
            rrw = width // 2
            rrh = height // 2
            PSMCT32Buffer = writeTexPSMCT32(0, rrw // 64, 0, 0, rrw, rrh, pixelBuffer)
            pixel = readTexPSMT8(0, width // 64, 0, 0, width, height, PSMCT32Buffer) 
        

'''

# Port Victor Suba's code to Python.
###=========================================================###
block32 = [
	 0,  1,  4,  5, 16, 17, 20, 21,
	 2,  3,  6,  7, 18, 19, 22, 23,
	 8,  9, 12, 13, 24, 25, 28, 29,
	10, 11, 14, 15, 26, 27, 30, 31
    ]


columnWord32 = [
	 0,  1,  4,  5,  8,  9, 12, 13,
	 2,  3,  6,  7, 10, 11, 14, 15
    ]

def writeTexPSMCT32(dbp, dbw, dsax, dsay, rrw, rrh, data):
    gsmem = bytearray(1024 * 1024 * 4)
    src = 0
    startBlockPos = dbp * 64
    for y in range(dsay + rrh):
        for x in range(dsax + rrw):    
            pageX = x // 64
            pageY = y // 32
            page = pageX + pageY * dbw

            px = x - (pageX * 64)
            py = y - (pageY * 32)

            blockX = px // 8
            blockY = py // 8
            block = block32[blockX + blockY * 8]

            bx = px - blockX * 8
            by = py - blockY * 8

            column = by // 2

            cx = bx
            cy = by - column * 2
            cw = columnWord32[cx + cy * 8]
            pos = startBlockPos + page * 2048 + block * 64 + column * 16 + cw
            gsmem[pos * 4:pos * 4 + 4] = data[src : src + 4]
            src += 4
    return gsmem
block4 =[
	 0,  2,  8, 10,
	 1,  3,  9, 11,
	 4,  6, 12, 14,
	 5,  7, 13, 15,
	16, 18, 24, 26,
	17, 19, 25, 27,
	20, 22, 28, 30,
	21, 23, 29, 31
]

columnWord4 =[
	[
		 0,  1,  4,  5,  8,  9, 12, 13,   0,  1,  4,  5,  8,  9, 12, 13,   0,  1,  4,  5,  8,  9, 12, 13,   0,  1,  4,  5,  8,  9, 12, 13,
		 2,  3,  6,  7, 10, 11, 14, 15,   2,  3,  6,  7, 10, 11, 14, 15,   2,  3,  6,  7, 10, 11, 14, 15,   2,  3,  6,  7, 10, 11, 14, 15,

		 8,  9, 12, 13,  0,  1,  4,  5,   8,  9, 12, 13,  0,  1,  4,  5,   8,  9, 12, 13,  0,  1,  4,  5,   8,  9, 12, 13,  0,  1,  4,  5,
		10, 11, 14, 15,  2,  3,  6,  7,  10, 11, 14, 15,  2,  3,  6,  7,  10, 11, 14, 15,  2,  3,  6,  7,  10, 11, 14, 15,  2,  3,  6,  7
	],
	[
		 8,  9, 12, 13,  0,  1,  4,  5,   8,  9, 12, 13,  0,  1,  4,  5,   8,  9, 12, 13,  0,  1,  4,  5,   8,  9, 12, 13,  0,  1,  4,  5,
		10, 11, 14, 15,  2,  3,  6,  7,  10, 11, 14, 15,  2,  3,  6,  7,  10, 11, 14, 15,  2,  3,  6,  7,  10, 11, 14, 15,  2,  3,  6,  7,

		 0,  1,  4,  5,  8,  9, 12, 13,   0,  1,  4,  5,  8,  9, 12, 13,   0,  1,  4,  5,  8,  9, 12, 13,   0,  1,  4,  5,  8,  9, 12, 13,
		 2,  3,  6,  7, 10, 11, 14, 15,   2,  3,  6,  7, 10, 11, 14, 15,   2,  3,  6,  7, 10, 11, 14, 15,   2,  3,  6,  7, 10, 11, 14, 15
	]
]

columnByte4 =[
	0, 0, 0, 0, 0, 0, 0, 0,  2, 2, 2, 2, 2, 2, 2, 2,  4, 4, 4, 4, 4, 4, 4, 4,  6, 6, 6, 6, 6, 6, 6, 6,
	0, 0, 0, 0, 0, 0, 0, 0,  2, 2, 2, 2, 2, 2, 2, 2,  4, 4, 4, 4, 4, 4, 4, 4,  6, 6, 6, 6, 6, 6, 6, 6,

	1, 1, 1, 1, 1, 1, 1, 1,  3, 3, 3, 3, 3, 3, 3, 3,  5, 5, 5, 5, 5, 5, 5, 5,  7, 7, 7, 7, 7, 7, 7, 7,
	1, 1, 1, 1, 1, 1, 1, 1,  3, 3, 3, 3, 3, 3, 3, 3,  5, 5, 5, 5, 5, 5, 5, 5,  7, 7, 7, 7, 7, 7, 7, 7
]
def readTexPSMT4(dbp, dbw, dsax, dsay, rrw, rrh, gsmem):
    data = bytearray(1024 * 1024 * 4)
    dbw >>= 1
    src = 0
    startBlockPos = dbp * 64

    odd = False

    for y in range(dsay + rrh):
        for x in range(dsax + rrw):  
		
            pageX = x // 128
            pageY = y // 128
            page = pageX + pageY * dbw

            px = x - (pageX * 128)
            py = y - (pageY * 128)

            blockX = px // 32
            blockY = py // 16
            block = block4[blockX + blockY * 4]

            bx = px - blockX * 32
            by = py - blockY * 16

            column = by // 4

            cx = bx
            cy = by - column * 4
            cw = columnWord4[column & 1][cx + cy * 32]
            cb = columnByte4[cx + cy * 32]
            pos = startBlockPos + page * 2048 + block * 64 + column * 16 + cw 
            pix = gsmem[pos * 4 + (cb >> 1)]

            if cb & 1:

                if odd:
                    data[src] = ((data[src]) & 0x0f) | (pix & 0xf0)
                else:
                    data[src] = ((data[src]) & 0xf0) | ((pix >> 4) & 0x0f)

            else:
                if odd:
                    data[src] = (data[src] & 0x0f) | (pix << 4) & 0xf0
                else:
                    data[src] = (data[src] & 0xf0) | (pix & 0x0f)

            
            if odd:
                src += 1

            odd = not odd

    return data

block8 = [
	 0,  1,  4,  5, 16, 17, 20, 21,
	 2,  3,  6,  7, 18, 19, 22, 23,
	 8,  9, 12, 13, 24, 25, 28, 29,
	10, 11, 14, 15, 26, 27, 30, 31
]

columnWord8 = [
	[
		 0,  1,  4,  5,  8,  9, 12, 13,   0,  1,  4,  5,  8,  9, 12, 13,
		 2,  3,  6,  7, 10, 11, 14, 15,   2,  3,  6,  7, 10, 11, 14, 15,

		 8,  9, 12, 13,  0,  1,  4,  5,   8,  9, 12, 13,  0,  1,  4,  5,
		10, 11, 14, 15,  2,  3,  6,  7,  10, 11, 14, 15,  2,  3,  6,  7
	],
	[
		 8,  9, 12, 13,  0,  1,  4,  5,   8,  9, 12, 13,  0,  1,  4,  5,
		10, 11, 14, 15,  2,  3,  6,  7,  10, 11, 14, 15,  2,  3,  6,  7,

		 0,  1,  4,  5,  8,  9, 12, 13,   0,  1,  4,  5,  8,  9, 12, 13,
		 2,  3,  6,  7, 10, 11, 14, 15,   2,  3,  6,  7, 10, 11, 14, 15
	]
]

columnByte8 = [

	0, 0, 0, 0, 0, 0, 0, 0,  2, 2, 2, 2, 2, 2, 2, 2,
	0, 0, 0, 0, 0, 0, 0, 0,  2, 2, 2, 2, 2, 2, 2, 2,

	1, 1, 1, 1, 1, 1, 1, 1,  3, 3, 3, 3, 3, 3, 3, 3,
	1, 1, 1, 1, 1, 1, 1, 1,  3, 3, 3, 3, 3, 3, 3, 3
]

def readTexPSMT8(dbp, dbw, dsax, dsay, rrw, rrh, gsmem):
    data = bytearray(1024 * 1024 * 4)
    dbw >>= 1
    src = 0
    startBlockPos = dbp * 64

    for y in range(dsay + rrh):
        for x in range(dsax + rrw):  
		
            pageX = x // 128
            pageY = y // 64
            page  = pageX + pageY * dbw

            px = x - (pageX * 128)
            py = y - (pageY * 64)

            blockX = px // 16
            blockY = py // 16
            block  = block8[blockX + blockY * 8]

            bx = px - blockX * 16
            by = py - blockY * 16

            column = by // 4

            cx = bx
            cy = by - column * 4
            cw = columnWord8[column & 1][cx + cy * 16]
            cb = columnByte8[cx + cy * 16]

            pos = startBlockPos + page * 2048 + block * 64 + column * 16 + cw
            data[src] = gsmem[pos * 4 + cb]
            src += 1
            
    return data
      
###=========================================================###



# Port Modified version Sparky's code to Python.
###=========================================================###
def unswizzle8(buf,width,height):
    out = bytearray(width*height)
    for y in range(height):
        for x in range(width):
            block_location = (y & (~0xf)) * width + (x & (~0xf)) * 2
            swap_selector = (((y + 2) >> 2) & 0x1) * 4
            posY = (((y & (~3)) >> 1) + (y & 1)) & 0x7
            column_location = posY * width * 2 + ((x + swap_selector) & 0x7) * 4
            byte_num = ((y >> 1) & 1) + ((x >> 2) & 2)
            swizzleid = block_location + column_location + byte_num
            out[y * width + x] = buf[swizzleid]
    return out
###=========================================================###


def unswizzle4(buffer, width, height):    
    pixels = bytearray(width * height)
    for i in range(width*height//2):
        index = buffer[i]
        id2 = (index >> 4) & 0xf
        id1 = index & 0xf
        pixels[i*2] = id1
        pixels[i*2+1] = id2
    newPixels = unswizzle8(pixels,width,height)    
    result = bytearray(width * height)
    for i in range(width*height//2):
            idx1 = newPixels[i*2+0]
            idx2 = newPixels[i*2+1]
            idx = ((idx2 << 4) | idx1) & 0xff
            result[i] = idx        
    return result

# only for 32bpp
def unswizzlePalette(palBuffer):  
    newPal = bytearray(1024)     
    for p in range(256):
        pos = ((p & 231) + ((p & 8) << 1) + ((p & 16) >> 1)) 
        newPal[pos*4:pos*4+4] = palBuffer[p*4:p*4+4]
    return newPal

# support 32bpp and 16bpp
def unswizzleCLUT(clutBuffer, bitsPerPiexl):
    bytesPerPixel = bitsPerPiexl // 8
    width = 16
    height = 16
    tileW = 8
    tileH = 2
    tileLineSize = tileW * bytesPerPixel
    numTileW = width // tileW
    numTileH = height // tileH
    newClutBuffer = bytearray(width * height * bytesPerPixel)
    offset = 0
    for y in range(numTileH):
        for x in range(numTileW):
            for ty in range(tileH):
                curHeight = y * tileH + ty
                curWidth = x * tileW
                dstPos = (curHeight * width + curWidth) * bytesPerPixel            
                newClutBuffer[dstPos:dstPos+tileLineSize] = clutBuffer[offset:offset+tileLineSize]
                offset += tileLineSize
    return newClutBuffer

# Convert 4bpp indexed to 8bpp indexed
def convert4bppto8bpp(buffer, width, height):
    pixels = bytearray(width * height)
    for i in range(width * height // 2):
        index = buffer[i]
        id2 = (index >> 4) & 0xf
        id1 = index & 0xf
        pixels[i*2] = id1
        pixels[i*2+1] = id2
    return pixels

# Read PS2 palette 32bit color
def readRGBA32(rawPixel):
    t = bytearray(4)
    t[0] = rawPixel & 0xFF
    t[1] = (rawPixel >>  8) & 0xFF
    t[2] = (rawPixel >> 16) & 0xFF
    t[3] = min(((rawPixel >> 24) & 0xFF) * 2, 255)
    return t
