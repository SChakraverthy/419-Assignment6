#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<unistd.h>
#include<sys/types.h>
#include<sys/socket.h>
#include<netdb.h>
#include<errno.h>

#define PORT "3650"

int sockfd, connfd;

int main(int argc, char** argv)
{
	struct addrinfo hints, *infoptr, *ptr;
	struct sockaddr_in clientaddr;
	socklen_t clientaddr_len;

	memset(&hints, 0, sizeof(hints));
	hints.ai_family = AF_INET;
	hints.ai_socktype = SOCK_STREAM;
	hints.ai_flags = AI_PASSIVE;

	int r = getaddrinfo(NULL, PORT, &hints, &infoptr);

	if (r)
	{
		fprintf(stderr, "getaddrinfo: %s\n", gai_strerror(r));
		exit(1);
	}

	for (ptr = infoptr; ptr != NULL; ptr = ptr->ai_next)
	{
		// Create a socket
		sockfd = socket(AF_INET, SOCK_STREAM, ptr->ai_protocol);
		if (sockfd == -1)
		{
			// Unsuccessfully attempted to create the socket.
			perror("Error: socket");
			continue;
		}

		printf("Socket created successfully!\n");

		// Bind the socket.
		if (bind(sockfd, ptr->ai_addr, ptr->ai_addrlen) == -1)
		{
			close(sockfd);
			perror("Error: bind");
			continue;
		}

		printf("Socket bound successfully!\n");

		break;
	}

	if (ptr == NULL)
	{
		fprintf(stderr, "Server: Failed to bind\n");
		exit(1);
	}

	// Listen for connections.
	if (listen(sockfd, 10) == -1)
	{
		close(sockfd);
		perror("Error: listen");
		exit(1);
	}

	printf("Server waiting for connections...\n");

	while (1)
	{

		clientaddr_len = sizeof(clientaddr);
		connfd = accept(sockfd, (struct sockaddr *)&clientaddr, &clientaddr_len);
		
		if (connfd == -1)
		{
			close(sockfd);
			close(connfd);
			perror("Error: accept");
			continue;
		}

		printf("Connected to a client!\n");
		close(connfd);
		break;
	}
	printf("Closed connection.\n");
	close(sockfd);
	return 0;

}