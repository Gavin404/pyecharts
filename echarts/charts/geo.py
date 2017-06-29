from echarts.base import Base

class Geo(Base):
    """
    <<< 地理坐标系组件 >>>
    地理坐标系组件用于地图的绘制，支持在地理坐标系上绘制散点图，线集。
    """
    def __init__(self, title="", subtitle="", **kwargs):
        super().__init__(title, subtitle, **kwargs)

    def add(self, *args, **kwargs):
        self.__add(*args, **kwargs)

    def __add(self, name, attr, value, *,
              type="scatter",
              maptype='china',
              symbol_size=12,
              border_color="#111",
              geo_normal_color="#323c48",
              geo_emphasis_color="#2a333d",
              effect_brushtype="stroke",
              effect_scale=2.5,
              effect_period=4, **kwargs):
        """

        :param name:
            图例名称
        :param attr:
            属性名称
        :param value:
            属性所对应的值
        :param type:
            图例类型，有 scatter/effectscatter 可选
        :param maptype:
            地图类型，目前只有 china 可选
        :param symbol_size:
            标记图形大小
        :param border_color:
            地图边界颜色
        :param geo_normal_color:
            正常状态下地图区域的颜色
        :param geo_emphasis_color:
            高亮状态下地图区域的颜色
        :param effect_brushtype:
            波纹绘制方式
        :param effect_scale:
            动画中波纹的最大缩放比例
        :param effect_period:
            动画的时间
        :param kwargs:
        """
        if isinstance(attr, list) and isinstance(value, list):
            assert len(attr) == len(value)
            _data = []
            for data in zip(attr, value):
                _name, _value = data
                if _name in self._geo_cities:
                    _v = self._geo_cities.get(_name)
                    _v.append(_value)
                    _value = list(_v)
                _data.append({"name": _name, "value": _value})
            self._option.update(
                geo={
                    "map": maptype,
                    "label": {},
                    "itemStyle": {"normal": {
                        "areaColor": geo_normal_color,
                        "borderColor": border_color},
                        "emphasis":{"areaColor": geo_emphasis_color}}
                })
            self._option.get('legend').get('data').append(name)
            if type == "scatter":
                self._option.get('series').append({
                    "type": type,
                    "name": name,
                    "coordinateSystem": 'geo',
                    "symbol": self.Option.symbol(**kwargs),
                    "symbolSize": symbol_size,
                    "data": _data,
                    "label": self.Option.label(**kwargs),
                })
            elif type == "effectscatter":
                self._option.get('series').append({
                    "type": type,
                    "name": name,
                    "coordinateSystem": 'geo',
                    "showEffectOn": "render",
                    "rippleEffect": {
                        "brushType": effect_brushtype,
                        "scale": effect_scale,
                        "period": effect_period
                    },
                    "symbol": self.Option.symbol(**kwargs),
                    "symbolSize": symbol_size,
                    "data": _data,
                    "label": self.Option.label(**kwargs),
                })
            self._legend_visualmap_colorlst(**kwargs)

