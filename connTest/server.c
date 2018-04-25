#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<unistd.h>
#include<sys/types.h>
#include<sys/socket.h>
#include<netdb.h>
#include<errno.h>

#define PORT "5100"

int main() 
{
	int sockfd, connfd;
	struct addrinfo hints, *infoptr, *ptr;
	struct sockaddr_in clientaddr;
	socklen_t clientaddr_len;

	// Set up the structures that we will use later.
	hints.ai_family = AF_INET;
	hints.ai_socktype = SOCK_STREAM;
	hints.ai_flags = AI_PASSIVE;

	int r = getaddrinfo(NULL, PORT, &hints, &infoptr);
	if (r != 0)
	{
		fprintf(stderr, "getaddrinfo:; %s\n", gai_strerror(r));
		exit(1);
	}

	// Loop through all the results and bind to one.
	for (ptr = infoptr; ptr != NULL; ptr = ptr->ai_next)
	{
		
		// Create socket.
		sockfd = socket(ptr->ai_family, ptr->ai_socktype, ptr->ai_protocol);
		if (sockfd == -1)
		{
			perror("Error: socket");
			continue;
		}

		// Bind
		if (bind(sockfd, ptr->ai_addr, ptr->ai_addrlen) == -1)
		{
			close(sockfd);
			perror("Error: bind");
			continue;
		}

		break;		
	}

	if (ptr == NULL) 
	{
		fprintf(stderr, "Unable to bind socket.\n");
		exit(1);
	}

	freeaddrinfo(infoptr);

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
		break;
	}
	close(connfd);
	close(sockfd);
	return 0;
}