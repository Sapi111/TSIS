-- add_phone
CREATE OR REPLACE PROCEDURE add_phone(p_name VARCHAR, p_phone VARCHAR, p_type VARCHAR)
LANGUAGE plpgsql AS $$
DECLARE cid INT;
BEGIN
    SELECT id INTO cid FROM contacts WHERE name = p_name;
    IF cid IS NULL THEN
        RAISE NOTICE 'Contact not found';
        RETURN;
    END IF;

    INSERT INTO phones(contact_id, phone, type)
    VALUES (cid, p_phone, p_type);
END;
$$;

-- move_to_group
CREATE OR REPLACE PROCEDURE move_to_group(p_name VARCHAR, p_group VARCHAR)
LANGUAGE plpgsql AS $$
DECLARE gid INT;
BEGIN
    SELECT id INTO gid FROM groups WHERE name = p_group;

    IF gid IS NULL THEN
        INSERT INTO groups(name) VALUES (p_group) RETURNING id INTO gid;
    END IF;

    UPDATE contacts SET group_id = gid WHERE name = p_name;
END;
$$;

-- search_contacts
CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE(name TEXT, email TEXT, phone TEXT) AS $$
BEGIN
    RETURN QUERY
    SELECT c.name, c.email, p.phone
    FROM contacts c
    LEFT JOIN phones p ON c.id = p.contact_id
    WHERE c.name ILIKE '%' || p_query || '%'
       OR c.email ILIKE '%' || p_query || '%'
       OR p.phone ILIKE '%' || p_query || '%';
END;
$$ LANGUAGE plpgsql;