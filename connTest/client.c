#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<unistd.h>
#include<sys/types.h>
#include<sys/socket.h>
#include<netdb.h>
#include<errno.h>

#define PORT "5100"

int main(int argc, char** argv)
{
	int sockfd;
	struct addrinfo hints, *infoptr, *ptr;
	struct sockaddr_in serveraddr;
	char* hostname;

	// Check that you are provided a hostname to connect to.
	if (argc != 2)
	{
		fprintf(stderr, "hostname\n");
		exit(1);
	}

	hostname = argv[1];

	// Set up the structures that we will use.
	memset(&hints, 0, sizeof(hints));
	hints.ai_family = AF_INET;
	hints.ai_socktype = SOCK_STREAM;

	int r = getaddrinfo(hostname, PORT, &hints, &infoptr);
	if (r != 0)
	{
		fprintf(stderr, "getaddrinfo: %s\n", gai_strerror(r));
		exit(1);
	}

	// Loop through the results and connect to the first address that we can.
	for (ptr = infoptr; ptr != NULL; ptr = ptr->ai_next)
	{

		// Create a socket.
		sockfd = socket(AF_INET, SOCK_STREAM, ptr->ai_protocol);
		if (sockfd == -1)
		{
			perror("Error: socket");
			close(sockfd);
			continue;
		}

		// Connect
		if (connect(sockfd, ptr->ai_addr, ptr->ai_addrlen) == -1)
		{
			perror("Error: connect");
			close(sockfd);
			continue;
		}

		printf("Client has connected to the server.\n");

		break;
	}

	if (ptr == NULL)
	{
		fprintf(stderr, "Unable to connect.\n");
		exit(1);
	}

	freeaddrinfo(infoptr);
}