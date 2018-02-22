DO $function$ 

DECLARE export_path VARCHAR = 'C:\TMP';
DECLARE replace_newline VARCHAR = '\n';
DECLARE replace_carriagereturn VARCHAR = '\r';
DECLARE error_message VARCHAR = '';

BEGIN 

RAISE NOTICE 'Start : %', timeofday();

--Uncommet for dev
DROP TABLE IF EXISTS tmp_LDV_Geo;
DROP TABLE IF EXISTS tmp_LDV_Export;

CREATE TEMPORARY TABLE tmp_LDV_Geo 
	--ON COMMIT DROP --Comment for dev
	AS SELECT
		rm.rijksmonument_nummer::INTEGER AS rijksmonument_nummer,
		ST_X(ST_Centroid(ST_CurveToLine(ST_Transform(g.gm_object, 28992))))::INTEGER obj_x_coord,
		ST_Y(ST_Centroid(ST_CurveToLine(ST_Transform(g.gm_object, 28992))))::INTEGER obj_y_coord,
		g.gm_object
	FROM
		sch_choi.cho c
	INNER JOIN sch_choi.rijksmonument rm ON rm.cho_id = c.cho_id AND rm.registratie_eind IS NULL
	LEFT JOIN sch_choi.geometrie g ON g.cho_id = c.cho_id AND g.registratie_eind IS NULL
	WHERE c.registratie_eind IS NULL
	ORDER BY rm.rijksmonument_nummer;

CREATE TEMPORARY TABLE tmp_LDV_Export 
	--ON COMMIT DROP --Comment for dev
	AS SELECT
		--Basis gegevens:
		rm.rijksmonument_nummer,
		nrm.rijksmonument_naam,
		regexp_replace(regexp_replace(o.omschrijving, replace_newline, '<n>', 'g'), replace_carriagereturn, '<r>', 'g') AS rijksmonument_omschrijving,
		
		--Adres:
		la.straat::VARCHAR AS straat,
		la.huisnummer::INTEGER AS huisnummer,
		(
			CASE
				WHEN la.huisletter IS NULL
				AND la.huisnummer_toevoeging IS NULL THEN NULL
				ELSE LTRIM(COALESCE( la.huisletter, '')|| COALESCE( ' ' || la.huisnummer_toevoeging, ''))
			END
		)::VARCHAR AS toevoeging,
		(
			LEFT(la.postcode, 4) || ' ' || RIGHT(la.postcode, 2)
		)::VARCHAR AS postcode,
		(
			CASE
				WHEN la.plaats_naam IS NULL THEN pl.plaatsnaam
				ELSE la.plaats_naam
			END
		)::VARCHAR AS plaats,
		pl.plaatsnaam AS brk_plaats,
		gem.gemeente AS brk_gemeente,
		prv.provinciecode AS brk_provincie,
		
		--Locatie:
		la.situering AS locatie_situering,
		ln.naam AS locatie_naam,
		regexp_replace(regexp_replace(lo.omschrijving, replace_newline, '<n>', 'g'), replace_carriagereturn, '<r>', 'g') AS locatie_omschrijving,
		
		--Complex gegevens:
		ttro.preflabel AS juridische_status,
		(
			CASE
				WHEN cpx.cho_id IS NULL THEN FALSE
				ELSE TRUE
			END
		)::BOOLEAN AS is_complex,
		cpx.complex_nummer AS complex_nummer,
		krcn.complex_naam AS complex_naam,
		regexp_replace(regexp_replace(krco.complex_omschrijving, replace_newline, '<n>', 'g'), replace_carriagereturn, '<r>', 'g') AS complex_omschrijving,
		
		--Kadastraal:
		rm.kio_datum::DATE AS kio_datum_inschrijving,
		rm.kio_deel::VARCHAR,
		rm.kio_nummer::INTEGER,
		
		--Geo:
		g.obj_x_coord AS X,
		g.obj_y_coord AS Y,
		g.gm_object AS geo
	FROM
		sch_choi.cho c
	INNER JOIN sch_choi.rijksmonument rm ON
		rm.cho_id = c.cho_id
		AND rm.registratie_eind IS NULL
	INNER JOIN tmp_LDV_Geo g ON
		g.rijksmonument_nummer = rm.rijksmonument_nummer
	INNER JOIN sch_thesauri.thesaurusterm ttro ON
		ttro.thesaurusterm_id = rm.juridische_status_id
		AND LOWER(ttro.preflabel) IN ('rijksmonument', 'voorbeschermd')
	LEFT JOIN sch_choi.basisregistratie brbag ON
		brbag.cho_id = c.cho_id
		AND brbag.registratie_eind IS NULL
	LEFT JOIN sch_choi.bag bag ON
		bag.basisregistratie_id = brbag.basisregistratie_id
		AND bag.registratie_eind IS NULL
		AND bag.hoofdadres = TRUE
	LEFT JOIN sch_choi.locatie_adres la ON
		la.bag_id = bag.bag_id
		AND la.registratie_eind IS NULL
		AND la.hoofdadres = TRUE
	LEFT JOIN(
			SELECT
				brpl.cho_id,
				STRING_AGG(pl.plaatsnaam, ',') plaatsnaam
			FROM
				sch_choi.basisregistratie brpl
			INNER JOIN sch_choi.brk_plaats pl ON
				pl.basisregistratie_id = brpl.basisregistratie_id
				AND pl.registratie_eind IS NULL
			WHERE
				brpl.registratie_eind IS NULL
			GROUP BY
				brpl.cho_id
		) pl ON
		pl.cho_id = c.cho_id
	LEFT JOIN(
			SELECT
				brgem.cho_id,
				STRING_AGG(gem.gemeente, ',') gemeente
			FROM
				sch_choi.basisregistratie brgem
			INNER JOIN sch_choi.brk_gemeente gem ON
				gem.basisregistratie_id = brgem.basisregistratie_id
				AND gem.registratie_eind IS NULL
			WHERE
				brgem.registratie_eind IS NULL
			GROUP BY
				brgem.cho_id
		) gem ON
		gem.cho_id = c.cho_id
	LEFT JOIN(
			SELECT
				brprv.cho_id,
				STRING_AGG(prv.provinciecode, ',') provinciecode
			FROM
				sch_choi.basisregistratie brprv
			INNER JOIN sch_choi.brk_provincie prv ON
				prv.basisregistratie_id = brprv.basisregistratie_id
				AND prv.registratie_eind IS NULL
			WHERE
				brprv.registratie_eind IS NULL
			GROUP BY
				brprv.cho_id
		) prv ON
		prv.cho_id = c.cho_id
	LEFT JOIN(
			SELECT
				l.cho_id,
				lo.omschrijving
			FROM
				sch_choi.locatie_aanduiding l
			INNER JOIN sch_choi.locatie_omschrijving lo ON
				lo.locatie_aanduiding_id = l.locatie_aanduiding_id
				AND lo.registratie_eind IS NULL
			WHERE
				l.registratie_eind IS NULL
				AND l.specialisatie_type_id = 10
		) lo ON
		lo.cho_id = c.cho_id
	LEFT JOIN(
			SELECT
				l.cho_id,
				ln.naam
			FROM
				sch_choi.locatie_aanduiding l
			INNER JOIN sch_choi.locatie_naam ln ON
				ln.locatie_aanduiding_id = l.locatie_aanduiding_id
				AND ln.registratie_eind IS NULL
			WHERE
				l.registratie_eind IS NULL
				AND l.specialisatie_type_id = 9
				AND l.registratie_verwijderd IS NULL 
		) ln ON
		ln.cho_id = c.cho_id
	LEFT JOIN(
			SELECT
				cho_id,
				regexp_replace(regexp_replace(omschrijving, replace_newline, '<n>', 'g'), replace_carriagereturn, '<r>', 'g') AS omschrijving
			FROM
				sch_kennis.kennisregistratie kr
			INNER JOIN sch_kennis.omschrijving o ON
				o.kennisregistratie_id = kr.kennisregistratie_id
			INNER JOIN sch_thesauri.thesaurusterm ttro ON
				ttro.thesaurusterm_id = o.omschrijvingstype_id
				AND LOWER(preflabel) = 'rijksmonumentomschrijving'
			WHERE
				kr.registratie_eind IS NULL
				AND kr.specialisatie_type_id = 8
				AND o.registratie_eind IS NULL
		) o ON
		o.cho_id = c.cho_id
	LEFT JOIN sch_choi.samenhang sh ON
		sh.cho_id_is_relatie_van = rm.cho_id
		AND sh.registratie_eind IS NULL
		AND relatie_type_id = 5640 --rm is onderdeel van complex
	LEFT JOIN sch_choi.complex cpx ON
		sh.cho_id_is_relatie_tot = cpx.cho_id
		AND cpx.registratie_eind IS NULL -- left join sch_kennis.legacy lc on lc.tabel='rijksmonument' and lc.pkveld='cho_id' and lc.pkwaarde=rm.cho_id::varchar and lc.lveld='obj_cbscode'
		-- left join sch_kennis.legacy lom on lom.tabel='rijksmonument' and lom.pkveld='cho_id' and lom.pkwaarde=rm.cho_id::varchar and lom.lveld='obj_cbsomschrijving'
	LEFT JOIN (SELECT krcn.cho_id, nc.naam AS complex_naam
		FROM sch_kennis.kennisregistratie krcn 
		INNER JOIN sch_kennis.naam nc ON krcn.kennisregistratie_id = nc.kennisregistratie_id AND nc.registratie_eind IS NULL AND nc.registratie_verwijderd IS NULL
		WHERE krcn.registratie_eind IS NULL AND krcn.registratie_verwijderd IS NULL AND krcn.formeel_standpunt = true) krcn ON krcn.cho_id = c.cho_id
	LEFT JOIN (SELECT krco.cho_id, oc.omschrijving AS complex_omschrijving
		FROM sch_kennis.kennisregistratie krco
		INNER JOIN sch_kennis.omschrijving oc ON krco.kennisregistratie_id=oc.kennisregistratie_id AND oc.registratie_eind IS NULL AND oc.registratie_verwijderd IS NULL
		WHERE krco.registratie_eind IS NULL AND krco.registratie_verwijderd IS NULL AND krco.formeel_standpunt = true) krco ON krco.cho_id = c.cho_id
	LEFT JOIN (SELECT kr.cho_id, nrm_1.naam AS rijksmonument_naam
		FROM sch_kennis.kennisregistratie kr
		JOIN sch_kennis.naam nrm_1 ON kr.kennisregistratie_id = nrm_1.kennisregistratie_id AND nrm_1.registratie_eind IS NULL AND nrm_1.registratie_verwijderd IS NULL
		WHERE kr.specialisatie_type_id = 6 AND kr.registratie_eind IS NULL AND kr.registratie_verwijderd IS NULL AND kr.formeel_standpunt = true) nrm ON nrm.cho_id = c.cho_id
	WHERE
		c.registratie_eind IS NULL
	ORDER BY
		rm.rijksmonument_nummer;

IF EXISTS(SELECT rijksmonument_nummer FROM tmp_LDV_Geo GROUP BY rijksmonument_nummer HAVING COUNT(*) > 1) THEN
	error_message = 'Primary Key niet uniek.';
END IF;

--Export data to .csv
execute FORMAT('COPY (SELECT * FROM tmp_LDV_Export ORDER BY rijksmonument_nummer) TO ''%s\LVD_Export.csv'' CSV HEADER DELIMITER ''|'' ENCODING ''WIN1252''', export_path);

--Regular query
--SELECT * FROM tmp_LDV_Export ORDER BY rijksmonument_nummer;

RAISE NOTICE 'Stop : %', timeofday();

IF length(COALESCE(error_message, '')) > 0 
THEN error_message = 'Fouten in export: ' || error_message || ' Einde Foutmelding.';
	EXECUTE FORMAT(
		'COPY (SELECT ''%s'') TO ''%s\error.txt'' ENCODING ''WIN1252''',
		error_message,
		export_path
	);
END IF;
END $function$;

SELECT * FROM tmp_LDV_Export;

--SELECT * FROM tmp_LDV_Export
----WHERE obj_juridische_status <> 'rijksmonument'
--WHERE rijksmonument_nummer = 100
----WHERE obj_complexnummer = 528915
----WHERE obj_complex_naam IS not null
--ORDER BY rijksmonument_nummer;