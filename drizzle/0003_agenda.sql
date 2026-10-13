CREATE TABLE `agenda_item` (
	`id` integer PRIMARY KEY AUTOINCREMENT NOT NULL,
	`canal_id` integer NOT NULL,
	`ordem` integer NOT NULL,
	`rotulo` text NOT NULL,
	`tipo` text NOT NULL,
	`dias_apos` integer NOT NULL,
	`hora` text NOT NULL,
	FOREIGN KEY (`canal_id`) REFERENCES `canal`(`id`) ON UPDATE no action ON DELETE cascade
);
--> statement-breakpoint
ALTER TABLE `canal` ADD `fuso_publico` text DEFAULT 'America/Sao_Paulo' NOT NULL;--> statement-breakpoint
INSERT INTO `agenda_item` (`canal_id`, `ordem`, `rotulo`, `tipo`, `dias_apos`, `hora`)
SELECT c.`id`, m.`ordem`, m.`rotulo`, m.`tipo`, m.`dias_apos`, m.`hora` FROM `canal` c, (
	SELECT 1 AS `ordem`, 'Short 1 (o corte mais forte)' AS `rotulo`, 'short' AS `tipo`, 0 AS `dias_apos`, '18:00' AS `hora`
	UNION ALL SELECT 2, 'Short 2', 'short', 1, '12:00'
	UNION ALL SELECT 3, 'Short 3', 'short', 2, '12:00'
	UNION ALL SELECT 4, 'Short 4', 'short', 4, '10:00'
	UNION ALL SELECT 5, 'Short da reserva (no 1º vídeo: o short 5 dele mesmo)', 'reserva', 5, '10:00'
) m;
