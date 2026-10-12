CREATE TABLE `dossie_item` (
	`id` integer PRIMARY KEY AUTOINCREMENT NOT NULL,
	`video_id` integer NOT NULL,
	`tipo` text NOT NULL,
	`ordem` integer DEFAULT 0 NOT NULL,
	`elemento` text NOT NULL,
	`categoria` text DEFAULT '' NOT NULL,
	`origem` text DEFAULT '' NOT NULL,
	`link` text DEFAULT '' NOT NULL,
	`base` text DEFAULT '' NOT NULL,
	`descricao` text DEFAULT '' NOT NULL,
	`contestacao` text DEFAULT '' NOT NULL,
	`provas` text DEFAULT '' NOT NULL,
	`risco` text DEFAULT 'baixo' NOT NULL,
	`mitigacao` text DEFAULT '' NOT NULL,
	FOREIGN KEY (`video_id`) REFERENCES `video`(`id`) ON UPDATE no action ON DELETE cascade
);
--> statement-breakpoint
CREATE INDEX `dossie_video` ON `dossie_item` (`video_id`,`tipo`);--> statement-breakpoint
ALTER TABLE `video` ADD `marcacao_sintetico` text DEFAULT 'nao-avaliado' NOT NULL;--> statement-breakpoint
ALTER TABLE `video` ADD `justificativa_sintetico` text DEFAULT '' NOT NULL;