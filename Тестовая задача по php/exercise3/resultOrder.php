<?php

    require_once 'generateFunction.php';
    require_once 'functionFile.php';

    function sortArr($a, $b)
    {
        //Функция для сортировки объектов
        //в порядке убывания
        if ($a->getArea() == $b->getArea()) {
          return 0;
        }
        return ($a->getArea() < $b->getArea()) ? 1 : -1;
    }

    //Выгрузка коллекции объектов из файла
    $arr = loadObj('resultObj.txt');

    //Сортировка в порядке убывания
    usort($arr, "sortArr");
    //Вывод результатов
    echo "Результат сортировки: </br></br>";

    foreach ($arr as $i => $item) {
        echo ($i + 1). ": $item->name". " ". $item->getArea();
        echo  " см<sup>2</sup>;</br>";
    }

    echo "</br>";
    echo '<a href="index.php">Сгенерировать новые объекты</a>';
