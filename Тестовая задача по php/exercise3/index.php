<?php

    require_once 'generateFunction.php';
    require_once 'functionFile.php';

    $minCountObj = 1; //Минимальное кол-во объеков
    $maxCountObj = 10; //Максимальное кол-во объеков
    $minNum = 1; //Минимальное случайное значение
    $maxNum = 100; //Максимальное случайное значение

    //Вызов функции генерации объектов
    $arrObj = generateObject($minCountObj, $maxCountObj,
        $minNum, $maxNum);
    //Сохранение коллекции объеков в файл
    safeObj($arrObj, 'resultObj.txt');

    echo "Сгенерировано объектов: ". count($arrObj). " шт. </br> </br>";
    echo '<a href="index.php">Новая генерация</a></br>';
    echo '<a href="resultOrder.php">Отсортировать
            по убыванию площади</a>';
