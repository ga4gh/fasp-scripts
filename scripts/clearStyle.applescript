tell application "Microsoft Excel"
	set gStyle to style "GA4GHStd" of workbook "DemoBanner.xlsx"
	set aStyle to style "GeneralAPI" of workbook "DemoBanner.xlsx"
	set pStyle to style "gaPlain" of workbook "DemoBanner.xlsx"
	set style object of cell 2 of row 3 of sheet 1 of workbook "DemoBanner.xlsx" to pStyle
	
end tell