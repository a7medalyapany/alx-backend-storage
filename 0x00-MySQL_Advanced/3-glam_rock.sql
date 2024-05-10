-- Calculate the lifespan of each band
SELECT band_name,
       (YEAR('2022-01-01') - YEAR(formed)) as lifespan
FROM bands
WHERE split = 'Glam rock'
ORDER BY lifespan DESC;
