/*******************************************************
 Windows HID simplification

 Alan Ott
 Signal 11 Software

 8/22/2009

 Copyright 2009, All Rights Reserved.

 This contents of this file may be used by anyone
 for any reason without any conditions and may be
 used as a starting point for your own applications
 which use HIDAPI.
********************************************************/

#include <stdio.h>
#include <wchar.h>
#include <string.h>
#include <stdlib.h>
#include "hidapi.h"

// Headers needed for sleeping.
#ifdef _WIN32
	#include <windows.h>
#else
	#include <unistd.h>
#endif

int main(int argc, char* argv[])
{
	int res;
	unsigned char buf[256];
	#define MAX_STR 255
	wchar_t wstr[MAX_STR];
	hid_device *handle;
	int i;

#ifdef WIN32
	UNREFERENCED_PARAMETER(argc);
	UNREFERENCED_PARAMETER(argv);
#endif


	// Open the device using the VID, PID,
	// and optionally the Serial number.
	////handle = hid_open(0x4d8, 0x3f, L"12345");
	handle = hid_open(0x057e, 0x0306, NULL);
	if (!handle) {
		printf("unable to open device\n");
 		return 1;
	}

	// Read the Manufacturer String
	wstr[0] = 0x0000;
	res = hid_get_manufacturer_string(handle, wstr, MAX_STR);
	if (res < 0)
		printf("Unable to read manufacturer string\n");
	printf("Manufacturer String: %ls\n", wstr);

	// Read the Product String
	wstr[0] = 0x0000;
	res = hid_get_product_string(handle, wstr, MAX_STR);
	if (res < 0)
		printf("Unable to read product string\n");
	printf("Product String: %ls\n", wstr);

	// Read the Serial Number String
	wstr[0] = 0x0000;
	res = hid_get_serial_number_string(handle, wstr, MAX_STR);
	if (res < 0)
		printf("Unable to read serial number string\n");
	printf("Serial Number String: (%d) %ls", wstr[0], wstr);
	printf("\n");

	// Read Indexed String 1
	wstr[0] = 0x0000;
	res = hid_get_indexed_string(handle, 1, wstr, MAX_STR);
	if (res < 0)
		printf("Unable to read indexed string 1\n");
	printf("Indexed String 1: %ls\n", wstr);

	// Set the hid_read() function to be non-blocking.
	hid_set_nonblocking(handle, 1);

	// Try to read from the device. There shoud be no
	// data here, but execution should not block.
	res = hid_read(handle, buf, 17);

	memset(buf,0,sizeof(buf));

	// Toggle LED (cmd 0x80). The first byte is the report number (0x1).
	buf[0] = 0x11;
	buf[1] = 0x20;
	res = hid_write_report(handle, buf, 2);
	if (res < 0) {
		printf("Unable to write()\n");
		printf("Error: %ls\n", hid_error(handle));
	}

	// Request state (cmd 0x81). The first byte is the report number (0x1).
	buf[0] = 0x15;
	buf[1] = 0x00;
	res = hid_write_report(handle, buf, 2);
	if (res < 0)
		printf("Unable to write() (2) %ls\n", hid_error(handle));

	// Read requested state. hid_read() has been set to be
	// non-blocking by the call to hid_set_nonblocking() above.
	// This loop demonstrates the non-blocking nature of hid_read().
	res = 0;
	while (res == 0) {
		res = hid_read(handle, buf, sizeof(buf));
		if (res == 0)
			printf("waiting...\n");
		if (res < 0)
			printf("Unable to read()\n");
		#ifdef WIN32
		Sleep(500);
		#else
		usleep(500*1000);
		#endif
	}

	printf("Data read:\n   ");
	// Print out the returned buffer.
	for (i = 0; i < res; i++)
		printf("%02hhx ", buf[i]);
	printf("\n");

#if 0
#endif // 0
    memset(buf,0,sizeof(buf));
	buf[0] = 0x16;
	buf[1] = 0x04;
	buf[2] = 0xa4;
	buf[3] = 0x00;
	buf[4] = 0xf0;
	buf[5] = 0x01;
	buf[6] = 0x55;
	res = hid_write_report(handle, buf, 22);
	if (res < 0)
		printf("Unable to write 0x55 to 0x(4)A400F0 %ls\n", hid_error(handle));

	res = 0;
	while (res == 0) {
		res = hid_read(handle, buf, sizeof(buf));
		if (res == 0)
			printf("waiting...\n");
		if (res < 0)
			printf("Unable to read()\n");
		#ifdef WIN32
		Sleep(500);
		#else
		usleep(500*1000);
		#endif
	}

    memset(buf,0,sizeof(buf));
	buf[0] = 0x16;
	buf[1] = 0x04;
	buf[2] = 0xa4;
	buf[3] = 0x00;
	buf[4] = 0xfb;
	buf[5] = 0x01;
	buf[6] = 0x00;
	res = hid_write_report(handle, buf, 22);
	if (res < 0)
		printf("Unable to write 0x00 to 0x(4)A400FB %ls\n", hid_error(handle));

	res = 0;
	while (res == 0) {
		res = hid_read(handle, buf, sizeof(buf));
		if (res == 0)
			printf("waiting...\n");
		if (res < 0)
			printf("Unable to read()\n");
		#ifdef WIN32
		Sleep(500);
		#else
		usleep(500*1000);
		#endif
	}
	// Read requested state. hid_read() has been set to be
	memset(buf,0,sizeof(buf));
	buf[0] = 0x17;
	buf[1] = 0x04;
	buf[2] = 0xa4;
	buf[3] = 0x00;
	buf[4] = 0xfa;
	buf[5] = 0x00;
	buf[6] = 0x06;
	res = hid_write_report(handle, buf, 22);
	if (res < 0)
		printf("Unable to write read_register %ls\n", hid_error(handle));
	// non-blocking by the call to hid_set_nonblocking() above.
	// This loop demonstrates the non-blocking nature of hid_read().
	res = 0;
	while (res == 0) {
		res = hid_read(handle, buf, sizeof(buf));
		if (res == 0)
			printf("waiting...\n");
		if (res < 0)
			printf("Unable to read()\n");
		#ifdef WIN32
		Sleep(500);
		#else
		usleep(500*1000);
		#endif
	}

	printf("Data read:\n   ");
	// Print out the returned buffer.
	for (i = 0; i < res; i++)
		printf("%02hhx ", buf[i]);
	printf("\n");
	printf("\n");
#if 0
#endif // 0

	hid_close(handle);

	/* Free static HIDAPI objects. */
	hid_exit();

#ifdef WIN32
	system("pause");
#endif

	return 0;
}
