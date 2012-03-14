///////////////////////////////////////////////////////////////////////////
// C++ code generated with wxFormBuilder (version Feb  9 2012)
// http://www.wxformbuilder.org/
//
// PLEASE DO "NOT" EDIT THIS FILE!
///////////////////////////////////////////////////////////////////////////

#ifndef __NONAME_H__
#define __NONAME_H__

#include <wx/artprov.h>
#include <wx/xrc/xmlres.h>
#include <wx/treectrl.h>
#include <wx/string.h>
#include <wx/gdicmn.h>
#include <wx/font.h>
#include <wx/colour.h>
#include <wx/settings.h>
#include <wx/listctrl.h>
#include <wx/listbox.h>
#include <wx/sizer.h>
#include <wx/panel.h>
#include <wx/textctrl.h>
#include <wx/splitter.h>
#include <wx/frame.h>

///////////////////////////////////////////////////////////////////////////


///////////////////////////////////////////////////////////////////////////////
/// Class main_frame
///////////////////////////////////////////////////////////////////////////////
class main_frame : public wxFrame 
{
	private:
	
	protected:
		wxSplitterWindow* main_panel;
		wxPanel* m_panel3;
		wxTreeCtrl* m_treeCtrl2;
		wxListCtrl* m_listCtrl1;
		wxListBox* m_listBox1;
		wxPanel* m_panel4;
		wxTextCtrl* m_textCtrl1;
	
	public:
		
		main_frame( wxWindow* parent, wxWindowID id = wxID_ANY, const wxString& title = wxEmptyString, const wxPoint& pos = wxDefaultPosition, const wxSize& size = wxSize( 1024,640 ), long style = wxDEFAULT_FRAME_STYLE|wxTAB_TRAVERSAL );
		
		~main_frame();
		
		void main_panelOnIdle( wxIdleEvent& )
		{
			main_panel->SetSashPosition( 200 );
			main_panel->Disconnect( wxEVT_IDLE, wxIdleEventHandler( main_frame::main_panelOnIdle ), NULL, this );
		}
	
};

#endif //__NONAME_H__
