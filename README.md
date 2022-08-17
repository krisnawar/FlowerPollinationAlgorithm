# Flower Pollination Algorithm

Flower pollination is an intriguing process in the natural world. Its evolutionary characteristics can be used to design new optimization algorithms. [Source](https://link.springer.com/chapter/10.1007/978-3-642-32894-7_27)

## What's in this repo

Implementation of Flower Pollination Algorithm using python to find the best coordinate to place pest controller device at the ricefield.

The ricefield coordinates are store in a csv file named sawah.csv. Initial device coordinates are hardcoded in the python file.

```python
uvus1 = [[66, 472], [83, 304], [203, 406], [202, 240], [272, 84]]
uvus2 = [[68, 472], [85, 304], [205, 406], [204, 240], [274, 84]]
uvus3 = [[66, 474], [83, 306], [203, 408], [202, 242], [272, 86]]
uvus4 = [[64, 474], [81, 306], [201, 408], [200, 242], [270, 86]]
```

At the end of the execution, the code will simply update the z_movement.csv file with z value changes based on the iteration. With this file, we can visualize the movement of the z value using Excel or any other apps.