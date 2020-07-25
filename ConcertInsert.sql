DELIMITER $$

# DROP PROCEDURE IF EXISTS ConcertInsert;

CREATE PROCEDURE ConcertInsert(
	IN event_json VARCHAR(3000)
)
BEGIN
	# Store event into database
    SET @event_time = JSON_EXTRACT(event_json, '$.time');
	INSERT IGNORE INTO t_event
	SET name    = JSON_EXTRACT(event_json, '$.name'),
    location    = JSON_EXTRACT(event_json, '$.location'),
    time        = JSON_EXTRACT(event_json, '$.time'),
    link        = JSON_EXTRACT(event_json, '$.link'),
    description = JSON_EXTRACT(event_json, '$.description');
	
    SET @test_time = JSON_EXTRACT(event_json, '$.time');
    
    SET @event_name = JSON_EXTRACT(event_json, '$.name');
    SET @event_id = (SELECT id_event FROM t_event WHERE name = @event_name);

    # Add new artists to DB
	SET @artist_list = JSON_EXTRACT(event_json, '$.artists');
    SET @c_artists = 0;
    
    WHILE @c_artists < JSON_LENGTH(@artist_list)
    DO
		SET @artist_name = JSON_EXTRACT(@artist_list, CONCAT('$[',@c_artists,']'));
        INSERT IGNORE INTO t_artist
        SET name_artist = @artist_name;
                
        # Set relation between artist and event in t_event_artist
		SET @artist_id = (SELECT id_artist FROM t_artist WHERE name_artist LIKE '%{@artist_name}%');
        
        IF @artist_id IS NOT NULL
			THEN
				INSERT INTO t_artist_event
				SELECT * FROM (SELECT @artist_id, @event_id) AS tmp
                WHERE NOT EXISTS (
					SELECT id_artist, id_event FROM t_artist_event WHERE id_artist = @artist_id AND id_event = @event_id
				);
		END IF;
                
        # Add artist event relation, if does not exist
        # INSERT INTO t_artist_event
        # SELECT * FROM (SELECT @artist_id, @event_id) AS tmp
        # WHERE NOT EXISTS (
		# 	SELECT id_artist, id_event FROM t_artist_event WHERE id_artist = @artist_id AND id_event = @event_id
        # );
        
        SET @c_artists = @c_artists + 1;   
    END WHILE;

	SET @genre_list = JSON_EXTRACT(event_json, '$.genres');
	SET @c_genres = 0;
    
	WHILE @c_genres < JSON_LENGTH(@genre_list)
    DO
		# add new genres to database
        SET @genre_name = JSON_EXTRACT(@genre_list, CONCAT('$[',@c_genres,']'));
		INSERT INTO t_genre (name_genre)
        SELECT * FROM (SELECT @genre_name) AS tmp
        WHERE NOT EXISTS (
			SELECT name_genre FROM t_genre WHERE name_genre = @genre_name
        );
        
        # Set relation between genre and event
        SET @genre_id = (SELECT id_genre FROM t_genre WHERE name_genre = @genre_name);
        INSERT IGNORE INTO t_genre_event
        SET id_genre = @genre_id,
        id_event = @event_id;
        SET @c_genres = @c_genres + 1;
    END WHILE;
    COMMIT;
END$$

DELIMITER ;