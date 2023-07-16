<?php

    function safeObj($value, $filename)
    {
        //Функция для сохранения коллекции объектов
        //в файл
        $str_value = serialize($value);

        $f = fopen($filename, 'w');
        fwrite($f, $str_value);
        fclose($f);
    }

    function loadObj($filename)
    {
        //Функция для извлечения объектов их файла
	      $file = file_get_contents($filename);
	      $value = unserialize($file);
	      return $value;
    }
