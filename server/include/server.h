/*
** EPITECH PROJECT, 2018
** PSU_zappy_2017
** File description:
** server.h
*/

#pragma once

#include <stddef.h>
#include "poll/src/common.h"
#include "list/src/list.h"

#define RBUFFER_SIZE 4096
#define CMD_SIZE 2048

typedef struct rbuf_s {
	char buffer[RBUFFER_SIZE];
	int start;
	int end;
	int size;
} rbuf_t;

typedef struct cmd_s {
	rbuf_t rbuf;
	char cmd[CMD_SIZE];
	char name[CMD_SIZE];
	char **param;
	int nparam;
} cmd_t;

typedef struct vec2_s {
	size_t x;
	size_t y;
} vec2_t;

typedef struct client_s {
	int fd;
	cmd_t cmd;
	size_t id;
	vec2_t pos;
	size_t food;
} client_t;

typedef struct control_s {
	poll_t *list;
	list_t *clients;
} control_t;
