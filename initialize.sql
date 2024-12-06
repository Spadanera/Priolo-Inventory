CREATE TABLE `bolle_uscita` (
    `PK_id_bolla` bigint NOT NULL AUTO_INCREMENT,
    `data_uscita` date NOT NULL,
    `stato` varchar(50) DEFAULT NULL,
    `note` text,
    `FK_id_cantiere_destinazione` bigint DEFAULT NULL COMMENT 'Destinazione',
    `conducente` varchar(255) DEFAULT NULL,
    `FK_targaMezzo` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
    PRIMARY KEY (`PK_id_bolla`),
    KEY `FK_id_cantiere` (`FK_id_cantiere_destinazione`),
    KEY `FK_targaMezzo` (`FK_targaMezzo`),
    CONSTRAINT `bolle_uscita_ibfk_1` FOREIGN KEY (`FK_id_cantiere_destinazione`) REFERENCES `cantieri` (`PK_id_cantiere`),
    CONSTRAINT `bolle_uscita_ibfk_2` FOREIGN KEY (`FK_targaMezzo`) REFERENCES `veicoli` (`PK_targa`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci

CREATE TABLE `cantieri` (
    `PK_id_cantiere` bigint NOT NULL AUTO_INCREMENT COMMENT 'Primary Key',
    `nome` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
    `nome2` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
    `indirizzo` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
    `ingegnere` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
    `supervisore` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
    `dataInizio` date DEFAULT NULL,
    `dataFine` date DEFAULT NULL,
    `numeroPiani` int DEFAULT NULL,
    `numeroServizi` int DEFAULT NULL,
    `capacitaPesoMassima` bigint DEFAULT NULL,
    PRIMARY KEY (`PK_id_cantiere`)
) ENGINE = InnoDB AUTO_INCREMENT = 9 DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci

CREATE TABLE `dettagli_bolle_uscita` (
    `PK_id_dettaglio` bigint NOT NULL AUTO_INCREMENT,
    `FK_id_bolla` bigint NOT NULL,
    `FK_id_prodotto` bigint NOT NULL,
    `quantita_uscita` bigint NOT NULL,
    `prezzo_totale` decimal(10, 2) DEFAULT NULL,
    PRIMARY KEY (`PK_id_dettaglio`),
    KEY `FK_id_bolla` (`FK_id_bolla`),
    KEY `FK_id_prodotto` (`FK_id_prodotto`),
    CONSTRAINT `dettagli_bolle_uscita_ibfk_1` FOREIGN KEY (`FK_id_bolla`) REFERENCES `bolle_uscita` (`PK_id_bolla`),
    CONSTRAINT `dettagli_bolle_uscita_ibfk_2` FOREIGN KEY (`FK_id_prodotto`) REFERENCES `prodotti` (`PK_id_prodotto`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci

CREATE TABLE `dettagli_ordini_fornitori` (
    `PK_id_dettaglio` bigint NOT NULL AUTO_INCREMENT,
    `FK_id_ordine` bigint NOT NULL,
    `FK_id_prodotto` bigint NOT NULL,
    `quantità_ordinata` bigint NOT NULL,
    `prezzo_totale` decimal(10, 2) DEFAULT NULL,
    `FK_id_cantiere` bigint DEFAULT NULL,
    PRIMARY KEY (`PK_id_dettaglio`),
    KEY `id_ordine` (`FK_id_ordine`),
    KEY `id_prodotto` (`FK_id_prodotto`),
    KEY `FK_id_cantiere` (`FK_id_cantiere`),
    CONSTRAINT `dettagli_ordini_fornitori_ibfk_1` FOREIGN KEY (`FK_id_ordine`) REFERENCES `ordini_fornitori` (`PK_id_ordine`),
    CONSTRAINT `dettagli_ordini_fornitori_ibfk_2` FOREIGN KEY (`FK_id_prodotto`) REFERENCES `prodotti` (`PK_id_prodotto`),
    CONSTRAINT `dettagli_ordini_fornitori_ibfk_3` FOREIGN KEY (`FK_id_cantiere`) REFERENCES `cantieri` (`PK_id_cantiere`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci

CREATE TABLE `fornitori` (
    `PK_id_fornitore` bigint NOT NULL AUTO_INCREMENT,
    `nome` varchar(100) NOT NULL,
    `contatti` varchar(255) DEFAULT NULL,
    `Indirizzo` varchar(255) DEFAULT NULL,
    `email` varchar(255) DEFAULT NULL,
    `codiceSDI` varchar(255) DEFAULT NULL,
    `partitaIva` varchar(255) DEFAULT NULL,
    `iban` varchar(255) DEFAULT NULL,
    `numeroTelefono` varchar(255) DEFAULT NULL,
    `Annotazioni` text,
    PRIMARY KEY (`PK_id_fornitore`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci

CREATE TABLE `ordini_clienti` (
    `PK_id_ordini` bigint NOT NULL AUTO_INCREMENT COMMENT 'Primary Key',
    `numeroFattura` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
    `valore` decimal(10, 2) DEFAULT NULL,
    `orderNumber` varchar(255) DEFAULT NULL,
    `item` bigint unsigned DEFAULT NULL,
    `soNumber` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
    `pos` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
    `lavorazioneDescrizione` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
    `FK_id_cantiere` bigint DEFAULT NULL COMMENT 'Foreign key',
    `stato` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
    `scadenza` date DEFAULT NULL,
    `extra` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci,
    `annotazioni` text,
    `extraDalPreventivoBool` bit(1) DEFAULT b'0',
    PRIMARY KEY (`PK_id_ordini`),
    KEY `FK_id_cantiere` (`FK_id_cantiere`),
    CONSTRAINT `ordini_clienti_ibfk_1` FOREIGN KEY (`FK_id_cantiere`) REFERENCES `cantieri` (`PK_id_cantiere`)
) ENGINE = InnoDB AUTO_INCREMENT = 44 DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci

CREATE TABLE `ordini_fornitori` (
    `PK_id_ordine` bigint NOT NULL AUTO_INCREMENT,
    `FK_id_fornitore` bigint NOT NULL,
    `data_ordine` date NOT NULL,
    `stato` varchar(50) DEFAULT 'In lavorazione',
    `conducenteNome` varchar(255) DEFAULT NULL,
    PRIMARY KEY (`PK_id_ordine`),
    KEY `id_fornitore` (`FK_id_fornitore`),
    CONSTRAINT `ordini_fornitori_ibfk_1` FOREIGN KEY (`FK_id_fornitore`) REFERENCES `fornitori` (`PK_id_fornitore`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci

CREATE TABLE `preventivi` (
    `PK_id_preventivo` bigint NOT NULL AUTO_INCREMENT COMMENT 'Primary Key',
    `numeroPreventivo` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
    `valorePreventivo` decimal(10, 2) DEFAULT NULL,
    `valoreExtraOpzionale` decimal(10, 2) DEFAULT NULL COMMENT 'solo se vi sono opere extra dal costo del preventivo. (ex: certificazione)',
    `scontoEffettuato` decimal(10, 2) DEFAULT '0.00',
    `FK_id_cantiere` bigint DEFAULT NULL,
    `stato` varchar(255) DEFAULT NULL,
    PRIMARY KEY (`PK_id_preventivo`),
    KEY `FK_idCantiere` (`FK_id_cantiere`),
    CONSTRAINT `preventivi_ibfk_1` FOREIGN KEY (`FK_id_cantiere`) REFERENCES `cantieri` (`PK_id_cantiere`)
) ENGINE = InnoDB AUTO_INCREMENT = 3 DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci

CREATE TABLE `prodotti` (
    `PK_id_prodotto` bigint NOT NULL AUTO_INCREMENT,
    `nome` varchar(100) NOT NULL,
    `modello` varchar(255) DEFAULT NULL,
    `marca` varchar(255) DEFAULT NULL,
    `prezzo` decimal(10, 2) DEFAULT NULL,
    `quantità_disponibile` bigint DEFAULT NULL,
    `codice_ean` varchar(255) DEFAULT NULL,
    `codice_altro` varchar(255) DEFAULT NULL,
    `sellerOrderNumber` varchar(255) DEFAULT NULL,
    `networkNumber` varchar(255) DEFAULT NULL,
    `CustomerOrderNumber` varchar(255) DEFAULT NULL,
    `PurchaseOrderNumber` varchar(255) DEFAULT NULL,
    `EquipmentNumber` varchar(255) DEFAULT NULL,
    `ProjectNumber` varchar(255) DEFAULT NULL,
    `ExternalIdentification` varchar(255) DEFAULT NULL,
    PRIMARY KEY (`PK_id_prodotto`),
    UNIQUE KEY `nome` (
        `nome`,
        `codice_ean`,
        `codice_altro`
    )
) ENGINE = InnoDB AUTO_INCREMENT = 3 DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci

CREATE TABLE `veicoli` (
    `PK_targa` varchar(20) NOT NULL,
    `nome` varchar(100) NOT NULL,
    `modello` varchar(100) NOT NULL,
    `marca` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
    `anno_immatricolazione` year NOT NULL,
    `colore` varchar(50) DEFAULT NULL,
    `tipo` varchar(50) DEFAULT NULL,
    `alimentazione` varchar(50) DEFAULT NULL,
    `chilometraggio` int DEFAULT NULL,
    `nextManutenzione` bigint DEFAULT NULL,
    `note` text,
    PRIMARY KEY (`PK_targa`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci