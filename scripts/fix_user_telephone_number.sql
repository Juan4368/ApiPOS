-- Identifica usuarios con telefono nulo o vacio
SELECT id, username, email, telephone_number
FROM "user"
WHERE telephone_number IS NULL
   OR btrim(telephone_number) = ''
ORDER BY id;

-- Ejemplo de correccion manual (ajusta el numero real antes de ejecutar)
-- UPDATE "user"
-- SET telephone_number = 'PENDIENTE'
-- WHERE id IN (1, 2, 3);
