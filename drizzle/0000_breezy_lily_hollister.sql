CREATE TABLE `canal` (
	`id` integer PRIMARY KEY AUTOINCREMENT NOT NULL,
	`nome` text NOT NULL,
	`nicho` text DEFAULT '' NOT NULL,
	`idioma` text DEFAULT 'pt-BR' NOT NULL,
	`prefixo_codigo` text NOT NULL,
	`pasta_relativa` text NOT NULL,
	`url_youtube` text,
	`youtube_channel_id` text,
	`modelo_descricao` text DEFAULT '' NOT NULL,
	`tags_padrao` text DEFAULT '[]' NOT NULL,
	`voz_padrao` text DEFAULT '' NOT NULL,
	`estilo_imagem_padrao` text DEFAULT '' NOT NULL,
	`referencias_identidade` text DEFAULT '' NOT NULL,
	`criado_em` integer DEFAULT (unixepoch() * 1000) NOT NULL
);
--> statement-breakpoint
CREATE UNIQUE INDEX `canal_prefixo_codigo_unique` ON `canal` (`prefixo_codigo`);--> statement-breakpoint
CREATE TABLE `cena` (
	`id` integer PRIMARY KEY AUTOINCREMENT NOT NULL,
	`video_id` integer NOT NULL,
	`ordem` integer NOT NULL,
	`trecho_roteiro` text DEFAULT '' NOT NULL,
	`prompt` text DEFAULT '' NOT NULL,
	`ferramenta` text DEFAULT '' NOT NULL,
	`arquivos` text DEFAULT '[]' NOT NULL,
	`status` text DEFAULT 'pendente' NOT NULL,
	`favorita` integer DEFAULT false NOT NULL,
	FOREIGN KEY (`video_id`) REFERENCES `video`(`id`) ON UPDATE no action ON DELETE cascade
);
--> statement-breakpoint
CREATE TABLE `checklist_item` (
	`id` integer PRIMARY KEY AUTOINCREMENT NOT NULL,
	`video_id` integer NOT NULL,
	`etapa` text NOT NULL,
	`ordem` integer NOT NULL,
	`texto` text NOT NULL,
	`feito` integer DEFAULT false NOT NULL,
	`feito_em` integer,
	FOREIGN KEY (`video_id`) REFERENCES `video`(`id`) ON UPDATE no action ON DELETE cascade
);
--> statement-breakpoint
CREATE TABLE `fonte` (
	`id` integer PRIMARY KEY AUTOINCREMENT NOT NULL,
	`video_id` integer NOT NULL,
	`titulo` text NOT NULL,
	`link_ou_referencia` text DEFAULT '' NOT NULL,
	`tipo` text NOT NULL,
	`fato_sustentado` text DEFAULT '' NOT NULL,
	`confiabilidade` text DEFAULT 'media' NOT NULL,
	`texto_tela` text DEFAULT '' NOT NULL,
	FOREIGN KEY (`video_id`) REFERENCES `video`(`id`) ON UPDATE no action ON DELETE cascade
);
--> statement-breakpoint
CREATE TABLE `fonte_cena` (
	`fonte_id` integer NOT NULL,
	`cena_id` integer NOT NULL,
	PRIMARY KEY(`fonte_id`, `cena_id`),
	FOREIGN KEY (`fonte_id`) REFERENCES `fonte`(`id`) ON UPDATE no action ON DELETE cascade,
	FOREIGN KEY (`cena_id`) REFERENCES `cena`(`id`) ON UPDATE no action ON DELETE cascade
);
--> statement-breakpoint
CREATE TABLE `formato` (
	`id` integer PRIMARY KEY AUTOINCREMENT NOT NULL,
	`canal_id` integer NOT NULL,
	`nome` text NOT NULL,
	`ativo` integer DEFAULT true NOT NULL,
	FOREIGN KEY (`canal_id`) REFERENCES `canal`(`id`) ON UPDATE no action ON DELETE cascade
);
--> statement-breakpoint
CREATE UNIQUE INDEX `formato_canal_nome` ON `formato` (`canal_id`,`nome`);--> statement-breakpoint
CREATE TABLE `grade_publicacao` (
	`id` integer PRIMARY KEY AUTOINCREMENT NOT NULL,
	`canal_id` integer NOT NULL,
	`dia_semana` integer NOT NULL,
	`hora` text NOT NULL,
	FOREIGN KEY (`canal_id`) REFERENCES `canal`(`id`) ON UPDATE no action ON DELETE cascade
);
--> statement-breakpoint
CREATE TABLE `historico_etapa` (
	`id` integer PRIMARY KEY AUTOINCREMENT NOT NULL,
	`video_id` integer NOT NULL,
	`etapa` text NOT NULL,
	`entrou_em` integer NOT NULL,
	FOREIGN KEY (`video_id`) REFERENCES `video`(`id`) ON UPDATE no action ON DELETE cascade
);
--> statement-breakpoint
CREATE TABLE `modelo_checklist` (
	`id` integer PRIMARY KEY AUTOINCREMENT NOT NULL,
	`canal_id` integer NOT NULL,
	`etapa` text NOT NULL,
	`ordem` integer NOT NULL,
	`texto` text NOT NULL,
	FOREIGN KEY (`canal_id`) REFERENCES `canal`(`id`) ON UPDATE no action ON DELETE cascade
);
--> statement-breakpoint
CREATE TABLE `prompt_banco` (
	`id` integer PRIMARY KEY AUTOINCREMENT NOT NULL,
	`canal_id` integer NOT NULL,
	`titulo` text NOT NULL,
	`prompt` text NOT NULL,
	`ferramenta` text DEFAULT '' NOT NULL,
	`cena_origem_id` integer,
	`arquivo_exemplo` text,
	FOREIGN KEY (`canal_id`) REFERENCES `canal`(`id`) ON UPDATE no action ON DELETE cascade,
	FOREIGN KEY (`cena_origem_id`) REFERENCES `cena`(`id`) ON UPDATE no action ON DELETE set null
);
--> statement-breakpoint
CREATE TABLE `serie` (
	`id` integer PRIMARY KEY AUTOINCREMENT NOT NULL,
	`canal_id` integer NOT NULL,
	`nome` text NOT NULL,
	`descricao` text DEFAULT '' NOT NULL,
	`youtube_playlist_id` text,
	FOREIGN KEY (`canal_id`) REFERENCES `canal`(`id`) ON UPDATE no action ON DELETE cascade
);
--> statement-breakpoint
CREATE TABLE `tema` (
	`id` integer PRIMARY KEY AUTOINCREMENT NOT NULL,
	`canal_id` integer NOT NULL,
	`nome` text NOT NULL,
	FOREIGN KEY (`canal_id`) REFERENCES `canal`(`id`) ON UPDATE no action ON DELETE cascade
);
--> statement-breakpoint
CREATE UNIQUE INDEX `tema_canal_nome` ON `tema` (`canal_id`,`nome`);--> statement-breakpoint
CREATE TABLE `titulo_candidato` (
	`id` integer PRIMARY KEY AUTOINCREMENT NOT NULL,
	`video_id` integer NOT NULL,
	`texto` text NOT NULL,
	`escolhido` integer DEFAULT false NOT NULL,
	FOREIGN KEY (`video_id`) REFERENCES `video`(`id`) ON UPDATE no action ON DELETE cascade
);
--> statement-breakpoint
CREATE TABLE `variante_thumbnail` (
	`id` integer PRIMARY KEY AUTOINCREMENT NOT NULL,
	`video_id` integer NOT NULL,
	`letra` text NOT NULL,
	`arquivo` text,
	`escolhida` integer DEFAULT false NOT NULL,
	`vencedora_teste` integer DEFAULT false NOT NULL,
	`percentual_tempo_exibicao` integer,
	FOREIGN KEY (`video_id`) REFERENCES `video`(`id`) ON UPDATE no action ON DELETE cascade
);
--> statement-breakpoint
CREATE UNIQUE INDEX `thumb_video_letra` ON `variante_thumbnail` (`video_id`,`letra`);--> statement-breakpoint
CREATE TABLE `versao_roteiro` (
	`id` integer PRIMARY KEY AUTOINCREMENT NOT NULL,
	`video_id` integer NOT NULL,
	`numero` integer NOT NULL,
	`conteudo` text NOT NULL,
	`origem` text NOT NULL,
	`nota` text,
	`arquivo_exportado` text,
	`criado_em` integer DEFAULT (unixepoch() * 1000) NOT NULL,
	FOREIGN KEY (`video_id`) REFERENCES `video`(`id`) ON UPDATE no action ON DELETE cascade
);
--> statement-breakpoint
CREATE UNIQUE INDEX `versao_video_numero` ON `versao_roteiro` (`video_id`,`numero`);--> statement-breakpoint
CREATE TABLE `video` (
	`id` integer PRIMARY KEY AUTOINCREMENT NOT NULL,
	`canal_id` integer NOT NULL,
	`numero` integer NOT NULL,
	`codigo` text NOT NULL,
	`titulo_provisorio` text NOT NULL,
	`titulo_final` text,
	`formato_id` integer,
	`serie_id` integer,
	`derivado_de_id` integer,
	`etapa` text DEFAULT 'Ideia' NOT NULL,
	`data_planejada` integer,
	`data_publicacao` integer,
	`nota_apelo` integer,
	`nota_ilustracao` integer,
	`nota_pesquisa` integer,
	`gancho` text DEFAULT '' NOT NULL,
	`resumo` text DEFAULT '' NOT NULL,
	`roteiro_atual` text DEFAULT '' NOT NULL,
	`pasta_relativa` text,
	`voz_usada` text DEFAULT '' NOT NULL,
	`duracao_final_seg` integer,
	`notas_corte` text DEFAULT '' NOT NULL,
	`descricao` text DEFAULT '' NOT NULL,
	`tags` text DEFAULT '[]' NOT NULL,
	`capitulos` text DEFAULT '' NOT NULL,
	`youtube_video_id` text,
	`url_youtube` text,
	`criado_em` integer DEFAULT (unixepoch() * 1000) NOT NULL,
	FOREIGN KEY (`canal_id`) REFERENCES `canal`(`id`) ON UPDATE no action ON DELETE cascade,
	FOREIGN KEY (`formato_id`) REFERENCES `formato`(`id`) ON UPDATE no action ON DELETE no action,
	FOREIGN KEY (`serie_id`) REFERENCES `serie`(`id`) ON UPDATE no action ON DELETE no action
);
--> statement-breakpoint
CREATE UNIQUE INDEX `video_codigo_unique` ON `video` (`codigo`);--> statement-breakpoint
CREATE UNIQUE INDEX `video_canal_numero` ON `video` (`canal_id`,`numero`);--> statement-breakpoint
CREATE INDEX `video_etapa` ON `video` (`canal_id`,`etapa`);--> statement-breakpoint
CREATE TABLE `video_tema` (
	`video_id` integer NOT NULL,
	`tema_id` integer NOT NULL,
	PRIMARY KEY(`video_id`, `tema_id`),
	FOREIGN KEY (`video_id`) REFERENCES `video`(`id`) ON UPDATE no action ON DELETE cascade,
	FOREIGN KEY (`tema_id`) REFERENCES `tema`(`id`) ON UPDATE no action ON DELETE cascade
);
