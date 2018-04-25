#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<unistd.h>
#include<sys/types.h>
#include<sys/socket.h>
#include<netdb.h>
#include<errno.h>

#define PORT "3650"


int main(int argc, char** argv)
{
	int sockfd;
	struct addrinfo hints, *infoptr, *ptr;
	struct sockaddr_in serveraddr;
	char* hostname;

	memset(&hints, 0, sizeof(hints));
	hints.ai_family = AF_INET;
	hints.ai_socktype = SOCK_STREAM;

	if (argc != 2)
	{
		fprintf(stderr, "Client: hostname \n");
		exit(1);
	}

	hostname = argv[1];

	memset(&hints, 0, sizeof(hints));
	hints.ai_family = AF_INET;
	hints.ai_socktype = SOCK_STREAM;

	int r = getaddrinfo(hostname, PORT, &hints, &infoptr);
	
	if (r)
	{
		fprintf(stderr, "getaddrinfo: %s\n", gai_strerror(r));
		exit(1);
	}

	for (ptr = infoptr; ptr != NULL; ptr = ptr->ai_next)
	{

		// Create the socket.
		sockfd = socket(AF_INET, SOCK_STREAM, ptr->ai_protocol);
		if (sockfd == -1)
		{
			perror("Error: socket");
			continue;
		}

		// Connect to the server
		if (connect(sockfd, ptr->ai_addr, ptr->ai_addrlen))
		{
			close(sockfd);
			perror("Error: connect");
			continue;
		}

		break;
	}

	if (ptr == NULL)
	{
		fprintf(stderr, "Client: Failed to locate host\n");
		exit(1);
	}

	freeaddrinfo(infoptr);

	printf("Client successfully connected to server!\n");
	close(sockfd);
	return 0;

}