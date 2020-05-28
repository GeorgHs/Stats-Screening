from abc import ABCMeta, abstractstaticmethod
from PortfolioScreen.Chart import Chart


class IChart(Chart):

    @abstractstaticmethod
    def get_dimensions():
        pass
        """The Chart Interface"""


class lineChart(IChart):
    def get_dimensions(self):
        return {"chartType": self.chartType, "timeHorizon": self.timeHorizon, "portfolio": self.portfolio}


class barChart(IChart):
    def get_dimensions(self):
        return {"chartType": self.chartType, "timeHorizon": self.timeHorizon, "portfolio": self.portfolio}


class pieChart(IChart):
    def get_dimensions(self):
        return {"chartType": self.chartType, "timeHorizon": self.timeHorizon, "portfolio": self.portfolio}


class Chart_Factory():

    @staticmethod
    def get_chart(charttype):
        try:
            if charttype == "line":
                return Chart('line', '2y', '')
            if charttype == "bar":
                return Chart('bar', '2y', '')
            if charttype == "pie":
                return Chart('pie', '2y', '')
            raise AssertionError('Chart not found')
        except AssertionError as _e:
            print(_e)


if __name__ == "__main__":
    CHART = Chart_Factory.get_chart("line")
    print(Chart.get_dimensions())
    CHART = Chart_Factory.get_chart("bar")
    print(Chart.get_dimensions())
    CHART = Chart_Factory.get_chart("pie")
    print(Chart.get_dimensions())
